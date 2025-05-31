from functools import wraps
from cachetools import TTLCache
from cachetools.keys import hashkey
from typing import Callable, Dict

# Global registry of caches keyed by (function, ttl)
_cache_registry: Dict[str, TTLCache] = {}


def cache(ttl_seconds: int = 900, maxsize: int = 100):
    """
    Decorator to cache function results with TTL (in seconds).
    Only one TTLCache per function+TTL combo will be created.
    """

    def decorator(func: Callable):
        cache_key = func.__qualname__
        if cache_key not in _cache_registry:
            _cache_registry[cache_key] = TTLCache(maxsize=maxsize, ttl=ttl_seconds)
        cache = _cache_registry[cache_key]

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Filter out 'db' from kwargs
            filtered_kwargs = {k: v for k, v in kwargs.items() if k != "db"}

            # Also remove positional 'db' if it appears in args
            args_without_db = tuple(
                arg
                for arg in args
                if not getattr(arg, "__class__", None).__name__.endswith("Session")
            )

            key = hashkey(func.__qualname__, *args_without_db, **filtered_kwargs)
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            return result

        return wrapper

    return decorator
