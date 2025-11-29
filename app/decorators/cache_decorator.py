from app.dependences.utils import count_ttl
from config import settings
from functools import wraps
from hashlib import sha256
import json

redis_client = settings.get_redis_client()


def make_cache_key(func_name, args, kwargs):
    def safe(obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        return None

    safe_args = [safe(a) for a in args]
    safe_kwargs = {k: safe(v) for k, v in kwargs.items()}
    return sha256(
        json.dumps((func_name, safe_args, safe_kwargs), sort_keys=True).encode()
    ).hexdigest()


def cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        key = make_cache_key(func.__name__, args, kwargs)
        print(key)
        data = await redis_client.get(key)
        if not data:
            data = await func(*args, **kwargs)
            await redis_client.setex(key, count_ttl(), json.dumps(data, default=str))
        else:
            data = json.loads(data)

        return data

    return wrapper
