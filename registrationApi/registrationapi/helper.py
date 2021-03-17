import re
import base64
import hashlib
from registrationapi.exceptions import DecodeError

def verify_email_regex(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex,email)

def is_valid_password(password):
    """
    Should have at least one number.
    Should have at least one uppercase and one lowercase character.
    Should have at least one special characters.
    Should be at least 6 characters long.
    """
    if (len(password) < 6):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password): 
        return False
    if not any(char.isdigit() for char in password):
        return False
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_']
    if not any(char in symbols for char in password):
        return False
    return True

def basicauth_decode(encoded_str):
    """Decode an encrypted HTTP basic authentication string. Returns a tuple of
    (username, password), and raises a DecodeError exception if nothing could be decoded.
    """
    split = encoded_str.strip().split(' ')
    # If split is only one element
    if len(split) == 1:
        try:
            username, password = base64.b64decode(split[0]).decode().split(':')
        except:
            raise DecodeError

    # If there are only two elements
    elif len(split) == 2:
        if split[0].strip().lower() == 'basic':
            try:
                username, password = base64.b64decode(split[1]).decode().split(':')
            except:
                raise DecodeError
        else:
            raise DecodeError
    # If there are more than 2 elements
    else:
        raise DecodeError

    return username, password

def basicauth_encode(id, password):
    return 'Basic ' + base64.b64encode((id + ':'+password).encode()).decode()

def hash_password(password):
    hashed = hashlib.sha256(password.encode())
    hashed_password = hashed.hexdigest()
    return hashed_password