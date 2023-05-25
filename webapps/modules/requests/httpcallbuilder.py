
from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpsession import HttpSession
from webapps.modules.requests.httpresponse import HttpResponseParser
from webapps.modules.requests.httpinterceptor import HttpInterceptor
from webapps.modules.requests.httpheadhandler import HttpHeadHandler

class HttpCallBuilder(object):

    def __init__(self, base_url: str = "", http_session: HttpSession = None) -> None:
        self._base_url = base_url
        self._http_session = http_session
        self._http_interceptor = None
        self._http_head_handler = None
        self._http_reponse_parser = None

    @property
    def base_url(self) -> str:
        return self._base_url
    
    @base_url.setter
    def base_url(self, base_url) -> None:
        self._base_url = base_url

    @property
    def http_session(self) -> str:
        return self._http_session
    
    @http_session.setter
    def http_session(self, http_session) -> None:
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


    def set_session(self, httpsession: HttpSession) -> None:
        self._http_session = httpsession
        
    def set_http_head_handler(self, handler: HttpHeadHandler) -> None:
        # TODO: verify handler
        self.http_head_handler = handler

    def set_response_parser(self, parser: HttpResponseParser) -> None:
        # TODO: verifi parser
        self.response_parser = parser
        
    def set_http_interceptor(self, interceptor: HttpInterceptor) -> None:
        # TODO: verify interceptor
        self._http_interceptor = interceptor


    def build(self, cls) -> HttpCall:
        # TODO: verify class
        http_call = cls()
        
        http_call.base_url = self.base_url
        http_call.http_session = self.http_session
        http_call.response_parser = self.response_parser

        if self.http_head_handler:
            http_call.set_head_handler(self._http_interceptor)
        
        if self.http_interceptor:
            http_call.set_http_interceptor(self._http_interceptor)

        return http_call