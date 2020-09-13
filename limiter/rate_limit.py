from time import time
from typing import List


class LimitDto:
    def __init__(self, max_requests, requests_made, reset_timestamp):
        self.max_requests = max_requests
        self.requests_made = requests_made
        self.reset_timestamp = reset_timestamp

    def __repr__(self):
        return str(self.__dict__)


def define_limiter_headers(max_requests, requests_made, seconds_until_reset):
    def define_limiter_headers_wrapper():
        return LimitDto(
            max_requests,
            requests_made,
            reset_timestamp=int(time()) + seconds_until_reset
        )

    return define_limiter_headers_wrapper


class RateLimit:
    def __init__(self, name, formatter, defaults):
        self.name = name
        self.max_requests: List = list(defaults[0])
        self.requests_made: List = list(defaults[1])
        self.reset_timestamp: List = [time() + default for default in defaults[2]]

        self._formatter = formatter

    def __repr__(self):
        return str(self.__dict__)

    def can_request(self) -> bool:
        if not (self.max_requests and self.requests_made and self.reset_timestamp):
            return True
        for max_requests, requests_made in zip(self.max_requests, self.requests_made):
            if requests_made >= max_requests:
                return False
        return True

    def is_initialized(self):
        if self.max_requests and self.requests_made and self.reset_timestamp:
            return True
        return False

    def set_formatter(self, callback):
        self._formatter = callback

    def register_request(self, request=None, headers: dict = None):
        if None not in (request, headers):
            raise Exception("Only one argument can't be none")

        if request is not None:
            headers = request.headers

        limits: List[LimitDto] = self._formatter(headers)

        for idx, limit in enumerate(limits):
            if idx > len(self.requests_made)-1:
                self.requests_made.append(limit.requests_made)
                self.max_requests.append(limit.max_requests)
                self.reset_timestamp.append(limit.reset_timestamp)

            self.requests_made[idx] = limit.requests_made
            self.max_requests[idx] = limit.max_requests

            if limit.requests_made == 1:
                self.reset_timestamp[idx] = limit.reset_timestamp

    @property
    def reset_in(self):
        times = []
        for reset_time in self.reset_timestamp:
            times.append(reset_time - int(time()))
        return times

    @property
    def time_until_new_request_is_possible(self):
        for idx, (max_requests, requests_made) in enumerate(zip(self.max_requests, self.requests_made)):
            if requests_made >= max_requests:
                return self.reset_timestamp[idx] - int(time())
