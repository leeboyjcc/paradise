import redis
import json
from functools import wraps
from time import sleep

class RedisCache:
    
    def __init__(self, redis_client):
        self._redis = redis_client

    def make_key(self, key):
        return "RedisCache:{}".format(key)

    def cache(self, timeout=0):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self.make_key(func.__name__)
                cache_value = self._redis.get(cache_key)
                if cache_value is None:
                    print('redis not cached')
                    value = func(*args, **kwargs)
                    if isinstance(timeout,int) and timeout > 0:
                        cache_value = json.dumps(value)
                        #self._redis.setex(cache_key, timeout, cache_value)
                        self._redis.set(cache_key, cache_value, timeout)
                else:
                    print('redis cached, key is {}'.format(cache_key))
                    value = json.loads(cache_value)
                return value
            return wrapper
        return decorator

r = redis.StrictRedis('localhost', 6379, charset='utf-8', decode_responses=True)
cache = RedisCache(r)

@cache.cache(timeout=10)
def execute():
    sleep(5)
    return {'python':10, 'flask':20}

if __name__ == '__main__':
    print(execute())

