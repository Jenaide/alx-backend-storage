#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    """
    a method that tracks the number of calls made to the Cache class.
    """
    def wrap(self, *args, **kwargs) -> Any:
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrap

class Cache:
    """
    storing an instance of the Redis client as a private variable
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        method that takes data arg and returns a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[bytes, None]:
        """
        a method that retrieves a value from a redis data storage.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        a method that retrieves a string value from redis
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        a method that retrieves an integer value from Redis
        """
        return self.get(key, fn=int)
