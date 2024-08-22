
from typing import Any, Callable, NoReturn, Self, Union

from httpx import Response

from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.modules.requests.httpsession import HttpSession



class HttpCall(object):

    _URL_PATH_ = "url_path"
    
    def __init__(self, base_url: str, api_path: str =None, api_method: str =None, http_session: HttpSession =None) -> None:
        self._base_url = base_url
        self._api_path = api_path
        self._api_method = api_method
        self._http_session = http_session
        self._interceptor_func = None
        self._parser_func = None
        self._response = None

    @property
    def base_url(self) -> str:
        return self._base_url
    
    @base_url.setter
    def base_url(self, base_url: str) -> None:
        self._base_url = base_url

    @property
    def api_path(self) -> str:
        return self._api_path
    
    @api_path.setter
    def api_path(self, api_path: str) -> None:
        self._api_path = api_path

    @property
    def api_method(self) -> str:
        return self._api_method
    
    @api_method.setter
    def api_method(self, api_method: str) -> None:
        self._api_method = api_method

    @property
    def response(self) -> bytes:
        return self._response
    
    @response.setter
    def response(self, response: bytes) -> None:
        self._response = response

    @property
    def http_session(self) -> HttpSession:
        return self._http_session
    
    @http_session.setter
    def http_session(self, http_session: HttpSession) -> None:
        self._http_session = http_session

    @property
    def http_interceptor(self) -> Callable[[Self, str, HttpHeaderPod, HttpSession], Self]:
        return self._interceptor_func
    
    @http_interceptor.setter
    def http_interceptor(self, parser: Callable[[Self, str, HttpHeaderPod, HttpSession], Self]) -> NoReturn:
        self._interceptor_func = parser

    @property
    def response_parser(self) -> Callable[[Self, Response, HttpHeaderPod, HttpSession, {}], Self]:
        return self._parser_func
    
    @response_parser.setter
    def response_parser(self, parser: Callable[[Self, Response, HttpHeaderPod, HttpSession, {}], Self]) -> NoReturn:
        self._parser_func = parser

    def set_session(self, http_session: HttpSession) -> Self:
        self._http_session = http_session
        return self

    def set_response_parser(self, parser: Callable[[Self, Response, HttpHeaderPod, HttpSession, {}], Self]) -> Self:
        self._parser_func = parser
        return self

    def set_http_interceptor(self, interceptor: Callable[[Self, str, HttpHeaderPod, HttpSession], Self]) -> Self:
        self._interceptor_func = interceptor
        return self

    def update_http_headers(self, headers: Union[dict, HttpHeaderPod], opt_in: tuple =None) -> Self:
        self._http_session.headers.update(headers, opt_in)
        return self
