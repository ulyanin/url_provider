import mas.repositories.cassandra_basic as cassandra_basic
from mas.helpers.random_key_generator import random_string
import mas.repositories.cacher as cacher

from typing import Any, Union


class AddKeyResult:
    msg = ''
    success = False
    key = None

    def __init__(self, *, key=None, msg=''):
        self.msg = msg
        self.success = len(msg) == 0
        self.key = key


async def get_url_by_key(*, url_id: str) -> Union[None, Any]:
    result = await cassandra_basic.get_url_by_key(key=url_id)
    for first_row in result:
        return first_row
    return None


async def add_custom_key_if_not_exists(*, url_to_short: str, custom_key: str) -> AddKeyResult:
    result = await cassandra_basic.add_custom_key(url=url_to_short, custom_key=custom_key)
    if isinstance(result, list):
        assert len(result) == 1
        result = result[0]
    if not result.applied:
        return AddKeyResult(msg=f"key '{custom_key}' alredy exists",)
    return AddKeyResult(key=custom_key)


async def add_random_key(*, url_to_short: str) -> AddKeyResult:
    random_key = await cacher.get_random_key(url=url_to_short)
    if random_key is not None:
        # cache hit
        return AddKeyResult(key=random_key)
    # try to generate unique random_key
    while True:
        random_key = random_string()
        result = await add_custom_key_if_not_exists(url_to_short=url_to_short, custom_key=random_key)
        if result.success:
            break
    # link random_key with url for caching
    added = await cassandra_basic.add_url_random_key(url=url_to_short, random_key=random_key)
    assert added is None
    return result


async def create() -> None:
    initial_script = cassandra_basic.read_initial_script()
    queries = initial_script.split(';')
    for query in queries:
        result = await cassandra_basic.execute(
            query=query,
        )
        print(f'query="{query}"\nresult={result}')
