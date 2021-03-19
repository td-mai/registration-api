"""
Test  api endpoints
"""
import io
import json
import unittest
from unittest import mock
from registrationapi import create_app
from registrationapi.helper import hash_password, basicauth_encode
from config import ConfigTest

REDIS_DB = {}
SQLDB = {}
def mock_sql_get_user_by_email(email):
    if email in SQLDB:
        return SQLDB[email]
    else:
        return None

def mock_redis_get_user(email):
    if email in REDIS_DB:
        return REDIS_DB[email]
    return None

def mock_redis_save_user(email, password, code, **kwargs):

    REDIS_DB[email] = {
        "email": email,
        "password": password,
        "activation_code": code
    }
    return True

def mock_send_email(email, code ):
    return 200

def mock_sql_create_user(email, password, username=None):
    SQLDB[email] = (email, password)
    return True


class TestApi(unittest.TestCase):

    @classmethod
    @mock.patch('registrationapi.dbqueries.get_user_by_email', side_effect = mock_sql_get_user_by_email)
    @mock.patch('registrationapi.redis.redis_get_user', side_effect = mock_redis_get_user)
    @mock.patch('registrationapi.redis.redis_save_user', side_effect = mock_redis_save_user)
    @mock.patch('registrationapi.email.send_email_activation_code', side_effect=mock_send_email)
    @mock.patch('registrationapi.dbqueries.create_user', side_effect=mock_sql_create_user)
    def setUpClass(self, get_user_by_email_mock, redis_get_user_mock, redis_save_user_mock,
        sendemail_mock, create_user_mock):

        "set up test fixtures"
        print('### Setting up flask server ###')
        app = create_app()
        app.config['TESTING'] = True
        app.config.from_object(ConfigTest())
        self.app = app.test_client()

    @classmethod
    def tearDownClass(self):
        "tear down test fixtures"
        print('### Tearing down the flask server ###')
        REDIS_DB = {}
        SQLDB = {}

    def test_get_register(self):
        "Methode not allowed"
        r = self.app.get('http://0.0.0.0:5000/api/register')
        self.assertEqual(r.status_code, 404)


    def test_01_post_register(self):
        "Email is already used"
        mock_sql_create_user("abc01@gmail.com", hash_password("pAss123*"))
        r = self.app.post('http://localhost:5000/api/register',
                            data=json.dumps({'email': "abc01@gmail.com", "password": "pAss123*"}),
                            headers= {'Content-type': 'application/json'})
        self.assertEqual(r.status_code, 409)

    
    def test_02_post_register(self):
        "Email is not valid"
        r = self.app.post('http://0.0.0.0:5000/api/register',
                            data=json.dumps({'email': "abcgmail.com", "password": "pAss123*"}),
                            headers= {'Content-type': 'application/json'})
        self.assertEqual(r.status_code, 422)
    
    
    def test_03_post_register(self):
        "Pasword is not valid"
        r = self.app.post('http://0.0.0.0:5000/api/register',
                            data=json.dumps({'email': "abcgmail.com", "password": "passs123"}),
                            headers= {'Content-type': 'application/json'})
        self.assertEqual(r.status_code, 422)

    
    def test_04_post_register(self):
        r = self.app.post('http://0.0.0.0:5000/api/register',
                            data=json.dumps({'email': "abc2@gmail.com", "password": "pAss123*"}),
                            headers= {'Content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

    
    def test_01_post_activate(self):
        r = self.app.post('http://localhost:5000/api/activate',
                        data=json.dumps({'code':1234}),
                        headers= {'Content-type': 'application/json'})
        self.assertEqual(r.status_code, 401)

    
    def test_02_post_activate(self):
        #user in redis
        mock_redis_save_user("user01@gmail.com", hash_password("45eez**AB"), 1234)

        r = self.app.post('http://localhost:5000/api/activate',
                        data=json.dumps({'code':1234}),
                        headers = {
                        'Authorization': basicauth_encode("user01@gmail.com", "45eez**AB"),
                        'Content-type': 'application/json',
                        'Accept': 'text/plain',
                        })              
        self.assertEqual(r.status_code, 201)
    
    def test_03_post_activate(self):
        mock_redis_save_user("user02@gmail.com", hash_password("45eez**AB"), 1234)

        "Wrong code"
        r = self.app.post('http://localhost:5000/api/activate',
                        data=json.dumps({'code':2345}),
                        headers = {
                        'Authorization': basicauth_encode("user02@gmail.com", "45eez**AB"),
                        'Content-type': 'application/json',
                        'Accept': 'text/plain',
                        })              
        self.assertEqual(r.status_code, 401)
    
    def test_05_post_activate(self):
        mock_redis_save_user("user02@gmail.com", hash_password("45eez**AB"), 1234)

        "Wrong Authorization header"
        r = self.app.post('http://localhost:5000/api/activate',
                        data=json.dumps({'code':2345}),
                        headers = {
                        'Authorization': basicauth_encode("user02@gmail.com", "abC123*"),
                        'Content-type': 'application/json',
                        'Accept': 'text/plain',
                        })              
        self.assertEqual(r.status_code, 401)

    def test_chain_register(self):

        r = self.app.post('http://0.0.0.0:5000/api/register',
                            data=json.dumps({'email': "abc@gmail.com", "password": "pASs123*"}),
                            headers= {'Content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)


        mock_redis_save_user("abc@gmail.com", hash_password( "pASs123*"), 7568)
        
        r2 = self.app.post('http://0.0.0.0:5000/api/activate',
                        data=json.dumps({'code':7568}),
                        headers = {
                        'Authorization': basicauth_encode("abc@gmail.com", "pASs123*"),
                        'Content-type': 'application/json',
                        'Accept': 'text/plain',
                        })              
        self.assertEqual(r2.status_code, 201)



