

from urllib.parse import urlsplit

from webapps.language.errors.httperror import HttpUrlNotValid

from webapps.modules.requests.httpcallbuilder import HttpCallBuilder
from webapps.modules.requests.httpinterceptor import HttpInterceptor
from webapps.modules.requests.httpsession import HttpSession
from webapps.modules.requests.httpresponse import HttpDefaultJsonParser, HttpResponseParser  
from webapps.modules.requests.httpheadhandler import HttpHeadHandler

class HttpCallRequests(object):
    
    def __init__(self) -> None:
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
    def http_head_handler(self) -> str:
        return self._http_head_handler
    
    @http_head_handler.setter
    def http_head_handler(self, handler) -> None:
        self._http_head_handler = handler

    @property
    def response_parser(self) -> str:
        return self._http_reponse_parser
    
    @response_parser.setter
    def response_parser(self, parser) -> None:
        self._http_reponse_parser = parser

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

    def set_base_url(self, base_url: str):
        # TODO: verify base url
        self._base_url = base_url
        return self

    def make_builder(self) -> HttpCallBuilder:
        try:
            url_structured = urlsplit(self.base_url)
        except Exception as error:
            # TODO : Handle exception
            raise HttpUrlNotValid(error.args)
        
        if not all((url_structured.scheme, url_structured.hostname, url_structured.path)):
            raise HttpUrlNotValid("Base url didn't carry all required fields")
        
        http_session = HttpSession(url_structured.scheme, url_structured.hostname, url_structured.geturl())

        builder = HttpCallBuilder(self.base_url, http_session)

        if self.http_head_handler:
            builder.http_head_handler = self.http_head_handler
        
        if self.response_parser:
            builder.response_parser = self.response_parser
        else:
            builder.response_parser = HttpDefaultJsonParser()

        if self.http_interceptor:
            builder.http_interceptor = self._http_interceptor

        return builder