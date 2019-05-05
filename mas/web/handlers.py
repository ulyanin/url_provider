from mas.repositories import cassandra_url_provider
import mas.settings as settings

from mas.helpers.statsd import statsd_client

from tornado.web import RequestHandler

import json
import urllib.parse
import traceback


def _construct_url(url_id):
    return urllib.parse.urlunparse((
        settings.DEFAULT_SCHEMA,
        f'{settings.DEFAULT_HOST}:{settings.DEFAULT_PORT}',
        settings.DEFAULT_GET_ADDR + url_id,
        None,
        None,
        None
    ))


class ErrorHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.set_header('Content-Type', 'application/json')
            if self.settings.get("serve_traceback") and "exc_info" in kwargs:
                # in debug mode, try to send a traceback
                lines = []
                for line in traceback.format_exception(*kwargs["exc_info"]):
                    lines.append(line)
                self.finish(json.dumps({
                    'error': {
                        'code': status_code,
                        'message': self._reason,
                        'traceback': lines,
                    }
                }))
            else:
                self.finish(json.dumps({
                    'error': {
                        'code': status_code,
                        'message': self._reason,
                    }
                }))


class ApiHandler(RequestHandler):
    # @tornado.gen.coroutine
    def get(self, path):
        self.write({
            'path': path
        })


class TestHandler(RequestHandler):
    async def get(self):
        key = 'aaaaa'
        ans = await cassandra_url_provider.get_url_by_key(url_id=key)
        if ans is None:
            self.set_status(404)
            self.write({
                'status': 'err',
                'msg': f'id "{key}" not found'
            })
            self.finish()
        else:
            self.redirect(url=ans.url, permanent=True)


class PingHandler(RequestHandler):
    _response = {
        'status': 'ok'
    }

    # @statsd_client.timer('ping-handler.execution-time')
    def get(self):
        # statsd_client.incr(self.__class__.__name__ + '.request')
        self.write(self._response)
        self.set_status(200)
        self.finish()


class DoShortUrl(RequestHandler):
    def _get_or_post_arg(self, key, default=None):
        value = self.body.get(key, default)
        value = self.get_argument(key, default=value)
        return value

    def _set_msg(self, msg: str):
        self.msg = msg

    def _bad_request(self, msg):
        self.set_status(400)
        self.write({
            'status': 'err',
            'msg': msg
        })
        self.finish()

    def initialize(self):
        self.msg = None
        self.body = {}
        try:
            if self.request.body:
                self.body = json.loads(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self._set_msg(msg=str(e))
        self.url_to_short = self._get_or_post_arg('url')
        self.custom_key = self._get_or_post_arg('key')

    def prepare(self):
        if self.msg:
            self._bad_request(self.msg)
        elif self.url_to_short is None:
            self._bad_request('pass &url by get or url by POST method')
        parsed_url = urllib.parse.urlparse(self.url_to_short)
        if not parsed_url.scheme:
            self.url_to_short = "http://" + self.url_to_short

    async def _do_request(self):
        # statsd_client.incr(self.__class__.__name__ + '.post')
        # with statsd_client.timer(self.__class__.__name__ + '.post'):
        if self.custom_key is None:
            result = await cassandra_url_provider.add_random_key(
                url_to_short=self.url_to_short,
            )
        else:
            result = await cassandra_url_provider.add_custom_key_if_not_exists(
                url_to_short=self.url_to_short,
                custom_key=self.custom_key
            )
        if not result.success:
            self.set_status(409)  # conflict
            self.write({
                'msg': result.msg,
                'status': 'err',
            })
        else:
            self.set_status(200)
            self.write({
                'short_url': _construct_url(result.key),
                'status': 'ok',
            })
        self.finish()

    async def post(self, *args, **kwargs):
        statsd_client.incr(self.__class__.__name__ + '.post')
        with statsd_client.timer(self.__class__.__name__ + '.post.time'):
            return await self._do_request()

    async def get(self, *args, **kwargs):
        statsd_client.incr(self.__class__.__name__ + '.get')
        with statsd_client.timer(self.__class__.__name__ + '.get.time'):
            return await self._do_request()


class GetShortUrl(RequestHandler):

    @statsd_client.timer('GetShortUrl.get.time')
    async def get(self, path, *args, **kwargs):
        print()
        statsd_client.incr(self.__class__.__name__ + '.post')
        if not path:
            self.set_status(400)
            self.write({
                'status': 'err',
                'msg': 'path is empty'
            })
        key = path
        ans = await cassandra_url_provider.get_url_by_key(url_id=key)
        if ans is None:
            self.set_status(404)
            self.write({
                'status': 'err',
                'msg': f"id '{key}' not found",
            })
        else:
            self.redirect(url=ans.url, permanent=True)
