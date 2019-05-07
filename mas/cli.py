import click
import tornado.ioloop
from tornado.web import Application
import tornado.web
import aioredis

import mas.settings as settings
from mas.web.urls import get_all_urls

import asyncio


class MyApplication(Application):
    def __init__(self, handlers, **kwargs):
        tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOMainLoop')
        super(MyApplication, self).__init__(handlers=handlers, **kwargs)

    def init_with_loop(self, loop):
        self.redis_url_to_random_key = loop.run_until_complete(
            aioredis.create_redis((settings.REDIS_HOST, 6379), loop=loop, db=0)
        )
        self.redis_url_by_random_key = loop.run_until_complete(
            aioredis.create_redis((settings.REDIS_HOST, 6379), loop=loop, db=1)
        )


@click.command()
@click.option('--port', default=settings.DEFAULT_PORT)
def serve(port: int):
    urls = get_all_urls()
    application = MyApplication(handlers=urls, debug=True)
    application.listen(port)

    loop = asyncio.get_event_loop()
    application.init_with_loop(loop)
    loop.run_forever()

    # loop = tornado.ioloop.IOLoop.current()
    # application.init_with_loop(loop)
    # loop.start()


if __name__ == '__main__':
    serve()
