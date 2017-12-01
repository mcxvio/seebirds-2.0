"""
Return previous searches from repository.
"""
import redis

def get_connection():
    r = None
    try:
        r = redis.Redis(
            host='localhost',
            port=6379)
            #, password='password')
        r.ping()
    except redis.exceptions.ConnectionError:
        r = None
        # todo: Log exception.

    return r

def save_key_value(key, value):
    if r != None:
        r.hset('default', key, value)

def get_values():
    data = None
    if r != None:
        data = r.hvals('default')
    return data

def get_values_nohash():
    if r != None:
        keys = r.execute_command('KEYS', '*')
        if len(keys) > 0:
            data = r.execute_command('MGET', *keys)
            return data
    return None

def clear_values():
    if r != None:
        r.flushdb()


r = get_connection()
