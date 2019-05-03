import mas.repositories.cassandra_basic as cassandra_basic

from typing import Any, Union


async def get_random_key_by_url(*, url: str) -> Union[None, Any]:
    result = await cassandra_basic.get_random_key_by_url(url=url)
    for first_row in result:
        return first_row
    return None
