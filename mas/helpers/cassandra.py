# proj

from mas.settings import CASSANDRA_CONNECTION_CONF
from mas.helpers.statsd import statsd_client

# libs
from aiocassandra import aiosession

import cassandra.io.asyncioreactor
import cassandra.policies
from cassandra.cluster import Cluster, Session

# common

from typing import Tuple, Any, List, Optional, Iterable, Union
import os
import uuid
import datetime

_cluster = None
_session = None
_prepared_get_url_by_key = None
_prepared_insert_url_random_key = None
_prepared_insert_url_key = None


def read_initial_script() -> str:
    with open(os.path.dirname(__file__) + 'create_tables.cql', 'r') as f:
        return f.read()


def get_session() -> Session:
    global _session, _cluster
    if _cluster is None:
        _cluster = Cluster(
            **CASSANDRA_CONNECTION_CONF,
            load_balancing_policy=cassandra.policies.RoundRobinPolicy()
        )
    if _session is None:
        _session = _cluster.connect('url_provider')
        aiosession(_session)
    return _session


async def _get_prepared_future(query: str) -> Any:
    session = get_session()
    return await session.prepare_future(query)


async def _prepare_get_url_by_key():
    global _prepared_get_url_by_key
    if _prepared_get_url_by_key is None:
        _prepared_get_url_by_key = await _get_prepared_future('SELECT * FROM key_to_url WHERE key=?')
    return _prepared_get_url_by_key


async def _prepare_insert_url_key():
    global _prepared_insert_url_key
    if _prepared_insert_url_key is None:
        _prepared_insert_url_key = await _get_prepared_future(
            '''INSERT INTO key_to_url (url, key, operation_id)
            VALUES (?, ?, ?)'''
        )
    return _prepared_insert_url_key


async def _prepare_insert_url_random_key():
    global _prepared_insert_url_random_key
    if _prepared_insert_url_random_key is None:
        _prepared_insert_url_random_key = await _get_prepared_future(
            '''INSERT INTO url_to_random_key (url, key)
            VALUES (?, ?)'''
        )
    return _prepared_insert_url_random_key


async def execute(
        *,
        query: str,
        values=None
) -> Any:
    session = get_session()
    prepared_query = await session.prepare_future(query)
    result = await session.execute_future(prepared_query, parameters=values)
    return result


async def get_url_by_key(
        *,
        key
) -> Iterable[Any]:
    prepared = await _prepare_get_url_by_key()
    session = get_session()
    result = await session.execute_future(prepared, parameters=[key])
    return result


async def add_custom_key(
        *,
        url: str,
        custom_key: str,
        operation_id: Union[uuid.UUID, None] = None
) -> bool:
    prepared = await _prepare_insert_url_key()
    session = get_session()
    result = await session.execute_future(
        prepared,
        parameters=[
            url,
            custom_key,
            operation_id if operation_id is not None else datetime.datetime.now()
        ]
    )
    return result
