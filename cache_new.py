import redis
import json
from functools import wraps
class RedisCache:

    def __init__(self, redis_client):
        self._redis_client = redis_client

    def cache(self, timeout=0):
        def decorator(f):
            @wraps(f)
            def inner(*args, **kwargs):
                if timeout <= 0:
                    return f(*args, **kwargs)

                key = f.__name__
                raw = self._redis_client.get(key)
                if raw is None:
                    value = f(*args, **kwargs)
                    self._redis_client.setex(key, timeout, json.dumps(value))
                    return value
                else:
                    #decode这里是将redis返回的字节串转为字符串
                    return json.loads(raw.decode())
            return inner
        return decorator
