from tornado.web import RequestHandler
from typing import List, Tuple

from mas.web.handlers import PingHandler, DoShortUrl, GetShortUrl, ApiHandler, TestHandler

ping_url = (r'/ping/', PingHandler)

custom_urls = [
    (r'/add', DoShortUrl),
    (r'/get/([^/]+)[/]{0,1}', GetShortUrl),
    (r'/api/([^/]+)[/]{0,1}', ApiHandler),
    (r'/test', TestHandler),
]


def get_all_urls() -> List[Tuple[str, RequestHandler]]:
    return custom_urls + [ping_url]
