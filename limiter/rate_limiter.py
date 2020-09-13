from functools import wraps
from time import sleep
from typing import List

from .rate_limit import RateLimit
from .exceptions import RateLimitHit


class OnHitAction:
    raise_exception = 0
    wait = 1


class RateLimiter:
    def __init__(self, storage=RateLimit, *, action=OnHitAction.raise_exception):
        self._limits = []
        self._storage = storage
        self.action = action

    def _create_single_limiter(self, name, callback, defaults=None):
        if defaults is None:
            defaults = [(), (), ()]
        self._limits.append(self._storage(name, callback, defaults))

    def create_limiter(self, names, callback, defaults=None):
        if isinstance(names, list):
            for name in names:
                self._create_single_limiter(name, callback, defaults)
        elif isinstance(names, str):
            self._create_single_limiter(names, callback, defaults)
        else:
            raise ValueError("names parameter must be either a string or a iterable")

    @staticmethod
    def can_request(limits):
        for limit in limits:
            print(limit, limit.can_request())
            if not limit.can_request():
                return [False, limit]
        return [True, None]

    @staticmethod
    def is_initialized(limits):
        for limit in limits:
            if not limit.is_initialized():
                return False
        return True

    @staticmethod
    def register_request(limits, rt):
        for limit in limits:
            limit.register_request(rt)

    def use(self, *limits_names):
        def request_wrapper(func):
            limits: List[RateLimit] = [limit for limit in self._limits if limit.name in limits_names]

            @wraps(func)
            def func_wrapper():
                rl = RateLimiter.can_request(limits)
                if rl[0]:
                    ret = func()
                    RateLimiter.register_request(limits, ret)
                    return ret
                else:
                    if self.action == OnHitAction.raise_exception:
                        raise RateLimitHit(rl[1])
                    elif self.action == OnHitAction.wait:
                        sleep(rl[1].time_until_new_request_is_possible)
                        ret = func()
                        RateLimiter.register_request(limits, ret)
                        return ret
            return func_wrapper
        return request_wrapper
