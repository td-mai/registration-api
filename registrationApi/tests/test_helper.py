import unittest
from registrationapi.helper import verify_email_regex, is_valid_password, basicauth_encode, basicauth_decode, hash_password
from registrationapi.exceptions import DecodeError

class TestHelperMethods(unittest.TestCase):

    def test_isEmailValid(self):
        email1 = "abc@dailymo.com"
        self.assertTrue(verify_email_regex(email1))
        email2 = "abcdailemo.com"
        self.assertFalse(verify_email_regex(email2))

    def test_isPasswordValid(self):
        pass1 = "abcA*123"
        self.assertTrue(is_valid_password(pass1))
        pass2 = "abcA123"
        self.assertFalse(is_valid_password(pass2))

    def test_basicauth_decode(self):
        encoded_str= "Basic YWJjQGdtYWlsLmNvbTo0NWVleioqMUE3Nzc="
        self.assertEqual(basicauth_decode(encoded_str), ("abc@gmail.com", "45eez**1A777"))

        encoded_wrong = "YWJjQGdtYWlsLmNvbTo0NWV"
        with self.assertRaises(DecodeError):
            basicauth_decode(encoded_wrong)
    
    def test_basicauth_encode(self):
        email, password = "abc@gmail.com", "45eez**1A777"
        self.assertEqual(basicauth_encode(email, password), "Basic YWJjQGdtYWlsLmNvbTo0NWVleioqMUE3Nzc=")
    
    def test_hashpassword(self):
        password = "Abc123*"
        self.assertEqual(hash_password(password),
            "ec98138a6cc21276570e1016f91fb1812801168149d19c7ce314551f835c9c1d")
