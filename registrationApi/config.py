"""Flask configuration."""
from os import environ, path
import json

basedir = path.abspath(path.dirname(__file__))

config_file = environ.get("CONFIG_FILE") or "config.json"

with open(config_file) as json_data_file:
    data_config = json.load(json_data_file)

class Config(object):
    """Set Flask config variables."""
    DEBUG = False
    TESTING = False

    DB_CONFIG = data_config["DB_CONFIG"]
    REDIS_CONFIG = data_config["REDIS_CONFIG"]

    SMTP_API_CONFIG = data_config["SMTP_API_CONFIG"]

    ACTIVATION_EMAIL_ADDR = data_config["ACTIVATION_EMAIL_ADDR"]

class ConfigProd(Config):
    ENV = "production"

class ConfigDev(Config):
    DEBUG = True
    ENV = "development"

class ConfigTest(Config):
    TESTING = True
    DB_CONFIG = {
        }
    REDIS_CONFIG = {
        }
    SMTP_API_CONFIG = {
        }

def get_config():
    if environ.get("FLASK_ENV") == "development":
        return ConfigDev()
    elif environ.get("FLASK_ENV") == "production":
        return ConfigProd()
    else:
        return ConfigTest()
