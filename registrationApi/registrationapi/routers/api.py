from flask import Blueprint, jsonify, request, url_for
from registrationapi.helper import hash_password, verify_email_regex, is_valid_password, basicauth_decode
from registrationapi.exceptions import *
from registrationapi.dbqueries import create_user, get_user_by_email
from registrationapi.redis import redis_save_user, redis_get_user
from registrationapi.email import send_email_activation_code
from random import randint

api = Blueprint('api', __name__)

@api.route('/api/register', methods=['POST'])
def register():
    request_data = request.get_json()
    if not request_data:
        raise ClientError("The email and password are required.", status_code=422)

    email = request_data.get("email")
    if not email:
        raise ClientError("The email is required.", status_code=422)
    
    if get_user_by_email(email):
        raise ClientError("This email is already used.", 409)

    password = request_data.get("password")
    if not password:
        raise ClientError("The password is required", status_code=422)
    if not verify_email_regex(email):
        raise ClientError("The email is not valid", status_code=422)

    if not is_valid_password(password):
        raise ClientError("The password is not valid."\
            " A valid password must be at least six characters long"\
                " and contain at least one uppercase, one lowercase character,"\
                    " one number and one special character.", status_code=422)


    #Generate activation code
    activation_code = randint(1000, 9999)
    try:
        redis_save_user(email, hash_password(password), activation_code)
    except Exception as err:
        raise ServerError(err.args, 500)
    #Send code by email
    try:
        send_email_activation_code(email, activation_code)
    except SendEmailError as err:
        raise ServerError(err.args, 500)

    response = jsonify({"email": email,
                        "status_code": 200})
    response.status_code = 200
    return response


@api.route('/api/activate', methods=['POST'])
def activate():
    if request.method == 'POST':
        encoded_str = request.headers.get('Authorization')

        if encoded_str is None :
            raise UnauthorizedError('Authorization header is required.')
        try:
            email, passwd = basicauth_decode(encoded_str)
        except DecodeError:
            raise UnauthorizedError("Wrong authorization header.")
        try:
            if get_user_by_email(email):
                raise ClientError("This account is already activated.", 409)
        except DatabaseError as err:
            raise ServerError(err.args, 500)
        
        request_data = request.get_json()
        if not request_data:
            raise ClientError("Activation code is required")
        received_code =request_data.get('code')
        if not received_code:
            raise ClientError("Activation code is required")
        
        user_dict = redis_get_user(email)
        if not user_dict:
            raise UnauthorizedError("The account does not exist or already expired."\
                " Please register again.")

        hashedpass = user_dict["password"]

        if hash_password(passwd) != hashedpass:
            raise UnauthorizedError("Wrong authorization header.")


        #Verify activation code
        if int(user_dict["activation_code"]) == int(received_code):
            #Create user in database
            try:
                create_user(email, hashedpass)
            except DatabaseIntegrityError as err:
                raise ClientError(err.args, 409)
            except DatabaseError as err:
                raise ServerError(err.args, 500)
        else:
            raise UnauthorizedError("Your activation code is incorrect. Please try again.")

        response = jsonify("User activated.")
        response.status_code = 201
        return response


@api.errorhandler(ApiException)
def handle_client_error(error):
    response = jsonify(error.__dict__)
    response.status_code = error.status_code
    return response