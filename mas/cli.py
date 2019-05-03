import click
from tornado import ioloop
from tornado.web import Application

from mas.settings import DEFAULT_PORT
from mas.web.urls import get_all_urls


@click.command()
@click.option('--port', default=DEFAULT_PORT)
def serve(port: int):
    urls = get_all_urls()
    application = Application(urls)
    application.listen(port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    serve()
