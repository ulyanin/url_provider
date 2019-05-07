import mas.repositories.cassandra_basic as cassandra_basic
from typing import Union
import aioredis


class AddKeyResult:
    msg = ''
    success = False
    key = None

    def __init__(self, *, key=None, msg=''):
        self.msg = msg
        self.success = len(msg) == 0
        self.key = key


async def get_random_key(*, url: str, redis=None) -> Union[None, str]:
    if redis is not None:
        value = await redis.get(url)
        if value is not None:
            return value.decode("utf-8")


async def add_random_key(*, url: str, random_key, redis) -> Union[None, str]:
    if redis is None:
        return
    return await redis.set(url, random_key)
