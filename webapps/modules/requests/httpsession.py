from typing import Generator
import httpx

from urllib.parse import ParseResult as UrlStructured

from httpx import Response
from http.cookiejar import Cookie, CookieJar

from webapps.modules.requests.dao.http_errors import HttpSessionInitialized
from webapps.modules.requests.httpheaderpod import HttpHeaderPod

class HttpSession(object):

    def __init__(self, scheme: str = "", hostname: str = "", sessionid: str = "", headers: HttpHeaderPod=None) -> None:
        self._url_object = None
        self._scheme = scheme
        self._hostname = hostname
        self._sessionid = sessionid

        if not headers:
            self._headers = HttpHeaderPod()
        else:
            self._headers = headers

        self._cookie_jar = CookieJar()

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
    def headers(self) -> HttpHeaderPod:
        return self._headers
    
    @headers.setter
    def headers(self, headers: HttpHeaderPod) -> None:
        self._headers = headers

    @property
    def cookies(self) -> Generator[Cookie, None, None]:
        return (cookie for cookie in self._cookie_jar)
    
    @cookies.setter
    def cookies(self, cookies: tuple[Cookie]) -> None:
        for cookie in cookies:
            self._cookie_jar.set_cookie_if_ok(cookie)

    @property
    def cookie_jar(self) -> Cookie:
        return self._cookie_jar
    
    @cookie_jar.setter
    def cookie_jar(self, cookiejar: CookieJar) -> None:
        self._cookie_jar = cookiejar

    def initialize(self, url: UrlStructured, sessionid: str) -> None:

        if not url:
            raise Exception(f"Invalid url {url}")

        if self.host:
            if self.host != url.host:
                raise HttpSessionInitialized(f"HTTP session with {self.host} have already been initialized as id: {self.sessionid}.")

        self.url = url
        self.scheme = url.scheme
        self.host = url.host
        self.sessionid = sessionid


    def draw_cookie_update(self, response: httpx.Response) -> CookieJar:
        jar = self._cookie_jar.extract_cookies(response)

        # TODO: deal with cookie jar
        return jar


    def supplement_headers(self, headers: dict) -> dict:
        return self._headers.union(headers)
