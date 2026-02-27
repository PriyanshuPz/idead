import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from flask import request, abort

P = ParamSpec("P")
R = TypeVar("R")

_rate_limits: dict[str, list[float]] = {}


def rate_limit(
    limit: int | Callable[[], int] = 5,
    per: int | Callable[[], int] = 60,
) -> Callable[[Callable[P, R]], Callable[P, R]]:

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
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
