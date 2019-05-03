import os
from typing import List, Any, Union
from asyncpg.exceptions import UniqueViolationError
import mas.helpers.cassandra as mhc
import uuid


class AddUrlResult:
    msg = ''
    result = None

    def __init__(self, *, msg='', result=None):
        assert msg or result
        self.msg = msg
        self.result = result


async def get(*, url_id: str) -> Union[None, Any]:
    result = await mhc.get_url_by_key(key=url_id)
    for first_row in result:
        return first_row
    return None


async def add(*, url_to_short: str) -> str:
    # await postgres.execute(
    #     query=_INSERT_QUERY,
    #     params=(user_id, object_id)
    # )
    return 'some_id'


async def add_custom_key_if_not_exists(*, url_to_short: str, custom_key: str) -> str:
    operation_id = uuid.uuid4()
    result = await mhc.add_custom_key(url=url_to_short, custom_key=custom_key, operation_id=operation_id)
    print(result)
    # now check whether this record was added by this query
    result = await get(url_id=custom_key)
    print('get=', result)
    print(result.operation_id)
    if result and result.operation_id == operation_id:
        return ''
    if result and result.operation_id != operation_id:
        return f'key "{custom_key}" alredy exists'
    return ''


async def create() -> None:
    initial_script = mhc.read_initial_script()
    queries = initial_script.split(';')
    for query in queries:
        result = await mhc.execute(
            query=query,
        )
        print(f'query="{query}"\nresult={result}')
