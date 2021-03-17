import redis
import json
from config import get_config
REDIS_CONFIG = get_config().REDIS_CONFIG
EX_SECONDS = 60

def redis_save_user(email, password, code, **kwargs):
    redisdb = redis.Redis(**REDIS_CONFIG)
    user_dict = {
        'email': email,
        'password': password,
        'activation_code': code,
    }
    user_dict.update(kwargs)
    redisdb.set(email, json.dumps(user_dict), ex=EX_SECONDS)

def redis_get_user(email):
    redisdb = redis.Redis(**REDIS_CONFIG)
    user_values = redisdb.get(email)
    if user_values:
        return json.loads(user_values)
    return None

def save_activation_code(email, code):
    redisdb = redis.Redis(**REDIS_CONFIG)
    redisdb.set(email, code, ex=EX_SECONDS)

def get_activation_code(email):
    redisdb = redis.Redis(**REDIS_CONFIG)
    return redisdb.get(email)