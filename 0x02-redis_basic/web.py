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
    def invoke(url) -> str:
        """
        a wrapper function for caching the output
        """
        redis_inst.incr(f'count:{url}')
        results = redis_inst.get(f'result:{url}')
        if results:
            return results.decode('utf-8')
        results = method(url)
        redis_inst.set(f'count:{url}', 0)
        redis_inst.setex(f'result:{url}', 10, results)
        return results
    return invoke

@cacher
def get_page(url: str) -> str:
    """
    function that returns the content of a url after caching the request
    """
    return requests.get(url).text


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
