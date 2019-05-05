import click
from tornado import ioloop
from tornado.web import Application
import tornado.web

from mas.settings import DEFAULT_PORT
from mas.web.urls import get_all_urls


class MyApplication(Application):
    def __init__(self, **kwargs):
        kwargs['debug'] = True
        super(MyApplication, self).__init__(**kwargs)


@click.command()
@click.option('--port', default=DEFAULT_PORT)
def serve(port: int):
    urls = get_all_urls()
    application = Application(urls, debug=True)
    application.listen(port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    serve()
