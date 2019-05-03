# from typing import Tuple, Any, List, Optional
#
# import asyncpg
# from asyncpg import Record
#
# from asyncpg.pool import Pool
#
# from mas.helpers.statsd import statsd_client
# from mas.settings import POSTGRES_CONNECTION_CONF
#
#
# async def create_pool() -> Pool:
#     return await asyncpg.create_pool(**POSTGRES_CONNECTION_CONF)
#
#
# _pool = None
#
#
# async def get_pool() -> Pool:
#     global _pool
#     if _pool is None:
#         _pool = await create_pool()
#     return _pool
#
#
# async def execute(
#         *,
#         query: str,
#         params: Optional[Tuple[Any, ...]] = None
# ) -> List[Record]:
#     with statsd_client.timer('postgres.execution_time'):
#         pool = await  get_pool()
#         async with pool.acquire() as connection:
#             return await connection.fetch(query, *params)
