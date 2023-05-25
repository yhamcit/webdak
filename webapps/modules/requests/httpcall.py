
from httpx import AsyncClient
from httpx import Response

from webapps.modules.requests.httpsession import HttpSession
from webapps.modules.requests.httpresponse import HttpResponseParser
from webapps.modules.requests.httpinterceptor import HttpInterceptor
from webapps.modules.requests.httpheadhandler import HttpHeadHandler



class HttpCall(object):
    
    def __init__(self, base_url: str = "", http_session: HttpSession = None) -> None:
        self._base_url = base_url
        self._http_session = http_session

    @property
    def base_url(self) -> str:
        return self._base_url
    
    @base_url.setter
    def base_url(self, base_url: str) -> None:
        self._base_url = base_url

    @property
    def http_session(self) -> HttpSession:
        return self._http_session
    
    @http_session.setter
    def http_session(self, http_session: HttpSession) -> None:
        self._http_session = http_session

    @property
    def http_head_handler(self) -> str:
        return self._http_head_handler
    
    @http_head_handler.setter
    def http_head_handler(self, handler) -> None:
        self._http_head_handler = handler

    @property
    def response_parser(self) -> str:
        return self._response_parser
    
    @response_parser.setter
    def response_parser(self, parser) -> None:
        self._response_parser = parser

    @property
    def http_interceptor(self) -> str:
        return self._http_interceptor
    
    @http_interceptor.setter
    def http_interceptor(self, interceptor) -> None:
        self._http_interceptor = interceptor

    @property
    def interceptor(self) -> HttpInterceptor:
        return self._interceptor
    
    @interceptor.setter
    def interceptor(self, interceptor: HttpInterceptor) -> None:
        self._interceptor = interceptor
