import requests
import json
from config import get_config
from registrationapi.exceptions import SendEmailError
from registrationapi.helper import basicauth_encode

config = get_config()
SMTP_API_CONFIG = config.SMTP_API_CONFIG
ACTIVATION_EMAIL_ADDR = config.ACTIVATION_EMAIL_ADDR

def sendemail(sender, receiver, text):
    data = {'sender': sender, 'receiver': receiver, 'text': text}
    auth_token = basicauth_encode(SMTP_API_CONFIG['user'], SMTP_API_CONFIG['password'])
    headers = {
        'Authorization': auth_token,
        'Content-type': 'application/json',
        'Accept': 'text/plain',
        }
    try:
        response = requests.post(SMTP_API_CONFIG["api_sendemail_url"],
                            data=json.dumps(data), 
                            headers=headers)
    except Exception as err:
        raise SendEmailError(err.args)

    if response.status_code not in [200, 201]:
        raise SendEmailError()

    return response.status_code

def send_email_activation_code(email, code):
    text = """ Your activation code is : <br> <b>{}</b><br>
        To activate your account please enter the code within 1 minute.""".format(code)
    r = sendemail(ACTIVATION_EMAIL_ADDR, email, text)
    return r
