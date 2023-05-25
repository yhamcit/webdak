
from typing import Any

from webapps.modules.requests.httpheaders import HttpHeaders

from webapps.modules.requests.httpsession import HttpSession
from webapps.modules.requests.httpresponse import HttpResponseParser
from webapps.modules.requests.httpinterceptor import HttpInterceptor
from webapps.modules.requests.httpheadhandler import HttpHeadHandler



class HttpCall(object):

    _URL_PATH_ = "url_path"
    
    def __init__(self, base_url: str, api_path: str =None, api_method: str =None, http_session: HttpSession =None) -> None:
        self._base_url = base_url
        self._api_path = api_path
        self._api_method = api_method
        self._http_session = http_session

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
    def http_envalue_set(self) -> dict:
        return self._http_envalue_set
    
    @http_envalue_set.setter
    def http_envalue_set(self, http_profile: dict) -> None:
        self._http_envalue_set = http_profile

    @property
    def http_session(self) -> HttpSession:
        return self._http_session
    
    @http_session.setter
    def http_session(self, http_session: HttpSession) -> None:
        self._http_session = http_session

    @property
    def env_value_set(self) -> dict:
        return self._env_value_set

    @property
    def http_head_handler(self) -> HttpHeadHandler:
        return self._http_head_handler
    
    @http_head_handler.setter
    def http_head_handler(self, handler: HttpHeadHandler) -> None:
        self._http_head_handler = handler

    @property
    def response_parser(self) -> HttpResponseParser:
        return self._response_parser
    
    @response_parser.setter
    def response_parser(self, parser: HttpResponseParser) -> None:
        self._response_parser = parser

    @property
    def http_interceptor(self) -> HttpInterceptor:
        return self._http_interceptor
    
    @http_interceptor.setter
    def http_interceptor(self, interceptor: HttpInterceptor) -> None:
        self._http_interceptor = interceptor

    def set_session(self, http_session: HttpSession) -> None:
        self.http_session = http_session
        return self
        
    def set_http_head_handler(self, handler: HttpHeadHandler) -> None:
        self.http_head_handler = handler
        return self

    def set_response_parser(self, parser: HttpResponseParser) -> None:
        self.http_reponse_parser = parser
        return self

    def set_http_interceptor(self, interceptor: HttpInterceptor) -> None:
        self.http_interceptor = interceptor
        return self

    def update_http_headers(self, headers: (dict, HttpHeaders), opt_in: tuple =None) -> None:
        self._http_session.headers.update(headers, opt_in)
        return self
