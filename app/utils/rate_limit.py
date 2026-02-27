import time
from functools import wraps
from flask import request, abort

_rate_limits = {}


def rate_limit(limit=5, per=60):
    """
    Rate limiting decorator.
    Allows `limit` requests per `per` seconds.
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            resolved_limit = limit() if callable(limit) else limit
            resolved_per = per() if callable(per) else per

            ip = request.remote_addr or "unknown"
            key = f"{request.endpoint}:{ip}"
            now = time.time()
            if key not in _rate_limits:
                _rate_limits[key] = []

            _rate_limits[key] = [t for t in _rate_limits[key] if now - t < resolved_per]

            if len(_rate_limits[key]) >= resolved_limit:
                abort(429, description="Rate limit exceeded. Try again later.")

            _rate_limits[key].append(now)
            return f(*args, **kwargs)

        return wrapped

    return decorator
