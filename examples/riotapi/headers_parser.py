from math import ceil
from time import time

from limiter.rate_limit import LimitDto


def parse_headers(raw_limits, raw_limits_count):
    limits = []
    for limit_count, limit, in zip(raw_limits_count.split(','), raw_limits.split(',')):
        [current_requests, reset_in_seconds] = limit_count.split(':')
        [max_requests, _] = limit.split(':')

        limits.append(LimitDto(
            int(max_requests),
            int(current_requests),
            ceil(time()) + int(reset_in_seconds)
        ))
    return limits
