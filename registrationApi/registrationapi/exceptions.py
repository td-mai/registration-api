from flask import jsonify

class ApiException(Exception):
    status_code = 400
    message = ""
    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

class ClientError(ApiException):
    pass

class ServerError(ApiException):
    pass

class UnauthorizedError(ClientError):
    status_code = 401
    message = "Unauthorized"


class DatabaseError(Exception):
    pass

class DatabaseIntegrityError(Exception):
    pass

class DecodeError(Exception):
    message = "Decode Error"

class SendEmailError(Exception):
    message = "Error in sending email."