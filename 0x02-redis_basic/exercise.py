#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    a method that tracks the number of calls made to the Cache class.
    """
    @wraps(method)
    def invoke(self, *args, **kwargs) -> Any:
        """
        a method that invokde given method after incrementation is called
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoke

def call_history(method: Callable) -> Callable:
    """
    a method that tracks a call details of a method if cached
    """
    @wraps(method)
    def invoke(self, *args, **kwargs) -> Any:
        """
        returns the methods output after storing 
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qua;name__ + ":outputs"

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return invoke

def reply(fn: Callable) -> None:
    """
    a function display the call history of the cache class
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    call_name = fn.__qualname__
    input_key = '{}:inputs'.format(call_name)
    output_key = '{}:outputs'.format(call_name)
    store_call_count = 0
    if redis_store.exists(call_name) != 0:
        store_call_count = int(redis_store.get(call_name))
    print('{} was called {} times:'.format(call_name, store_call_count))
    call_inputs = redis_store.lrange(input_key, 0, -1)
    call_outputs = redis_store.lrange(output_key, 0, -1)
    for call_input, call_output in zip(call_inputs, call_outputs):
        print('{}(*{}) -> {}'.format(
            call_name,
            call_input.decode("utf-8"),
            call_output,
        ))

class Cache:
    """
    storing an instance of the Redis client as a private variable
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
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
