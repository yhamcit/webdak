

from urllib.parse import urlsplit
from webapps.modules.requests.dao.http_errors import HttpInvalidUrl
from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpheaders import HttpHeaders
from webapps.modules.requests.httpsession import HttpSession
from webapps.modules.requests.httpresponse import HttpResponseParser
from webapps.modules.requests.httpinterceptor import HttpInterceptor
from webapps.modules.requests.httpheadhandler import HttpHeadHandler



class HttpCallBuilder(object):

    def __init__(self, base_url: str = "", http_session: HttpSession = None) -> None:
        self._base_url = base_url

        try:
            url_structured = urlsplit(self.base_url)
        except Exception as error:
            # TODO : Handle exception
            raise HttpInvalidUrl(error.args)
        
        if not all((url_structured.scheme, url_structured.hostname, url_structured.path)):
            raise HttpInvalidUrl("Base url didn't carry all required fields")

        if http_session:
            self._http_session = http_session
        else:
            self._http_session = HttpSession(url_structured.scheme, url_structured.hostname, url_structured.geturl())

        self._http_interceptor = None
        self._http_head_handler = None
        self._http_reponse_parser = None

    @property
    def base_url(self) -> str:
        return self._base_url
    
    @base_url.setter
    def base_url(self, base_url: str) -> None:
        self._base_url = base_url

    @property
    def http_session(self) -> str:
        return self._http_session
    
    @http_session.setter
    def http_session(self, http_session: HttpSession) -> None:
        if not http_session:
            raise Exception(f"Invalide http session: {http_session} ")

        self._http_session = http_session

    @property
    def http_head_handler(self) -> str:
        return self._http_head_handler
    
    @http_head_handler.setter
    def http_head_handler(self, http_head_handler: HttpHeadHandler) -> None:
        if not http_head_handler:
            raise Exception(f"Invalide http head handler: {http_head_handler} ")
        
        self._http_head_handler = http_head_handler

    @property
    def response_parser(self) -> str:
        return self._http_reponse_parser
    
    @response_parser.setter
    def response_parser(self, parser: HttpResponseParser) -> None:
        if not parser:
            raise Exception(f"Invalide http parser: {parser} ")
        
        self._http_reponse_parser = parser

    @property
    def http_interceptor(self) -> HttpInterceptor:
        return self._http_interceptor
    
    @http_interceptor.setter
    def http_interceptor(self, interceptor: HttpInterceptor) -> None:
        if not interceptor:
            raise Exception(f"Invalide http interceptor{interceptor} ")
        
        self._http_interceptor = interceptor

    @property
    def headers(self) -> HttpHeaders:
        return self._http_session.headers
    
    @headers.setter
    def headers(self, headers: HttpHeaders) -> None:
        self._http_session.headers = headers

    def build(self, cls, env_pack: dict, api_path: str =None, api_method: str =None, http_session: HttpSession=None, interceptor: HttpInterceptor=None, parser: HttpResponseParser=None) -> HttpCall:

        assert issubclass(cls, HttpCall)
        http_call = cls(self.base_url, api_path =api_path, api_method =api_method)

        if env_pack:
            pass

        if http_session:
            http_call.http_session = http_session
        else:
            http_call.http_session = self._http_session
        
        if interceptor:
            http_call.http_interceptor = interceptor
        elif self.http_interceptor:
            http_call.http_interceptor = self._http_interceptor

        if parser:
            http_call.response_parser = parser
        elif self.response_parser:
            http_call.response_parser = self._http_reponse_parser
        
        return http_call