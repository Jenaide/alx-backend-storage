#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""
import redis
import uuid
from typing import Union


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
