
from urllib import parse as urlparser
from urllib.parse import ParseResult as UrlStructured

from httpx import Response

from webapps.language.errors.httperror import HttpSessionInitialized
from webapps.modules.requests.httpcookie import HttpCookie, HttpCookieJar
from webapps.modules.requests.httpheaders import HttpHeaders

class HttpSession(object):

    def __init__(self, scheme: str = "", hostname: str = "", sessionid: str = "") -> None:
        self._url_object = None
        self._scheme = scheme
        self._hostname = hostname
        self._sessionid = sessionid
        self._headers = HttpHeaders()
        self._cookies = HttpCookie()
        self._cookiejar = self.cookies.cookiejar

    @property
    def url(self) -> UrlStructured:
        return self._url_object

    @url.setter
    def url(self, url: UrlStructured) -> None:
        self._url_object = url

    @property
    def scheme(self) -> str:
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: str) -> None:
        self._scheme = scheme

    @property
    def host(self) -> str:
        return self._hostname

    @host.setter
    def host(self, host: str) -> None:
        self._hostname = host

    @property
    def sessionid(self) -> str:
        return self._sessionid
    
    @sessionid.setter
    def sessionid(self, sessionid: str) -> None:
        self._sessionid = sessionid

    @property
    def headers(self) -> HttpHeaders:
        return self._headers
    
    @headers.setter
    def headers(self, headers: HttpHeaders) -> None:
        self._headers = headers

    @property
    def cookies(self) -> HttpCookie:
        return self._cookies

    @property
    def cookiejar(self) -> HttpCookieJar:
        return self._cookiejar
    
    @cookies.setter
    def cookiejar(self, cookiejar: HttpCookieJar) -> None:
        self._cookiejar = cookiejar

    def initialize(self, url: UrlStructured, sessionid: str) -> None:
        # TODO: verify url_object

        if self.host:
            if self.host != url.host:
                raise HttpSessionInitialized(
                    "HTTP session with {host} have already been initialized as id: {sessionid}."\
                        .format(host = self.host, sessionid = self.sessionid))

        self.url = url
        self.scheme = url.scheme
        self.host = url.host
        self.sessionid = sessionid


    def draw_cookie_update(self, response: Response) -> None:
        self.cookies.extract_cookies(response)

    def make_headers(self, headers: dict) -> dict:
        return self.headers.merge(headers)


    