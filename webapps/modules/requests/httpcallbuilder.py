

from urllib.parse import urlsplit
from webapps.modules.requests.dao.http_errors import HttpInvalidUrl
from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.modules.requests.httpsession import HttpSession



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
    def headers(self) -> HttpHeaderPod:
        return self._http_session.headers
    
    @headers.setter
    def headers(self, headers: HttpHeaderPod) -> None:
        self._http_session.headers = headers

    def build(self, cls, api_path: str =None, api_method: str =None) -> HttpCall:

        assert issubclass(cls, HttpCall)
        http_call = cls(self.base_url, api_path =api_path, api_method =api_method)

        http_call.http_session = self._http_session

        return http_call