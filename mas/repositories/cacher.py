import mas.repositories.cassandra_basic as cassandra_basic
from mas.helpers.random_key_generator import random_string

from typing import Any, Union


class AddKeyResult:
    msg = ''
    success = False
    key = None

    def __init__(self, *, key=None, msg=''):
        self.msg = msg
        self.success = len(msg) == 0
        self.key = key


async def get_random_key(*, url: str) -> Union[None, str]:
    # cache from cassandra
    result = await cassandra_basic.get_random_key_by_url(url=url)
    for first_row in result:
        return first_row.key
    return None
