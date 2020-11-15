from collections import namedtuple

import requests
import aiohttp

from examples.riotapi.headers_parser import parse_headers
from limiter import RateLimiter
from limiter.rate_limiter import OnHitAction

API_KEY = '<api_key>'


def app_limits(headers):
    raw_limits = headers['X-App-Rate-Limit']
    raw_limits_count = headers['X-App-Rate-Limit-Count']
    return parse_headers(raw_limits, raw_limits_count)


def method_app_limits(headers):
    raw_limits = headers['X-Method-Rate-Limit']
    raw_limits_count = headers['X-Method-Rate-Limit-Count']
    return parse_headers(raw_limits, raw_limits_count)


limiter = RateLimiter(action=OnHitAction.wait)
limiter.create_limiter('App', app_limits)
limiter.create_limiter(['SummonerV4', 'MatchV4'], method_app_limits)


def get_summoner():
    @limiter.use('App', 'SummonerV4')
    def get_summoner_req():
        req = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/its%20andre', headers={
            'X-Riot-Token': API_KEY
        })
        return req

    return get_summoner_req()


async def get_summoner_async():
    @limiter.use('App', 'SummonerV4')
    async def get_summoner_async_req():
        async with aiohttp.ClientSession() as session:
            async with session.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/its%20andre',
                                   headers={
                                       'X-Riot-Token': API_KEY
                                   }) as req:
                return namedtuple("Request", ["headers", "json", "status_code"])(req.headers, await req.json(),
                                                                                 req.status)

    return await get_summoner_async_req()
