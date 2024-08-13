import functools
import time
from typing import Callable, Coroutine


class CacheStore:
    def __init__(self):
        self.cache = {}

    def set_value(self, key: tuple, result):
        self.cache[key] = (result, time.time())

    def is_cached(self, key: tuple) -> bool:
        return key in self.cache

    def get_cached_result(self, key: tuple, lifetime: int):
        result, timestamp = self.cache[key]

        if time.time() - timestamp <= lifetime:
            return result

        del self.cache[key]


cache_store = CacheStore()


def async_cache(lifetime: int = 60):
    def wrapper(func: Callable[..., Coroutine]):

        @functools.wraps(func)
        async def inner(*args, **kwargs):
            key = (func, frozenset(kwargs.items()))

            if cache_store.is_cached(key):
                result = cache_store.get_cached_result(key, lifetime)

                if result:
                    return result

            result = await func(*args, **kwargs)
            cache_store.set_value(key, result)

            return result

        return inner

    return wrapper
