#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""
import redis
import requests
from typing import Callable
from functools import wraps
redis_inst = redis.Redis() # redis instance



def cacher(method: Callable) -> Callable:
    """
    caches the output data when fetched
    """
    @wraps(method)
    def invoke(*args, **kwargs):
        """
        a wrapper function for caching the output
        """
        url = args[0]
        redis_inst.incr(f'count:{url}')
        results = redis_inst.get(f'{url}')
        if results:
            return results.decode('utf-8')
        redis_inst.setex(f'{url}, 10, {method(url)}')
        return method(*args, **kwargs)
    return invoke

@cacher
def get_page(url: str) -> str:
    """
    function that returns the content of a url after caching the request
    """
    return requests.get(url).text


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
