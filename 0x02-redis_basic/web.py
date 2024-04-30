#!/usr/bin/env python3
"""Module containing function to return HTML content of a particular URL"""
import requests
import time
from functools import wraps

def cache_with_tracking(func):
    cache = {}

    @wraps(func)
    def wrapper(url):
        # Check if the URL is in cache and if it's not expired
        if url in cache and time.time() - cache[url]['timestamp'] < 10:
            cache[url]['count'] += 1
            return cache[url]['content']
        else:
            content = func(url)
            cache[url] = {'content': content, 'timestamp': time.time(), 'count': 1}
            return content

    return wrapper

@cache_with_tracking
def get_page(url):
    response = requests.get(url)
    return response.text

# Test the function
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com"
    for _ in range(3):
        print(get_page(url))

    # Wait for cache expiration
    time.sleep(11)

    # Access the same URL again
    print(get_page(url))
