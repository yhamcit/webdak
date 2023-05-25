
from httpx import AsyncClient
from httpx import Response

from urllib.parse import urlsplit
from urllib.parse import urlencode
from urllib.parse import parse_qs as urlsplit_qs
from urllib.parse import urljoin
from urllib.parse import quote
from urllib.parse import SplitResult

from webapps.modules.asyncoroutine.promisepool import PromisePool

from webapps.language.errors.httperror import HttpUrlNotValid
from webapps.modules.requests.httpcookie import HttpCookie
from webapps.modules.requests.httpheaders import HttpHeaders
from webapps.modules.requests.httpsession import HttpSession


class HttpMethods(object):
    
    def __init__(self, api_path: str = "", headers: dict = {}, cookies = (), auth = None) -> None:
        self._api_path = api_path
        self._headers = headers
        self._cookies = cookies

    @property
    def api_path(self) -> str:
        return self._api_path

    @property
    def headers(self) -> str:
        return self._headers

    @property
    def cookies(self) -> str:
        return self._cookies

    @api_path.setter
    def api_path(self, api_path) -> None:
        self._api_path = api_path

    def finalize_url(self, base_url, path_template, params = {}, fragment = "", urlargv: dict = {}) -> str:
        try:
            api_path = path_template.format(**urlargv)
            split_result = urlsplit(api_path)
            result_query = urlsplit_qs(split_result.query)

            for key, value in result_query:
                if key in params:
                    v = params[key]
                    value.extend(v) if isinstance(v, list) else value.append(v)
            
            relative_url = SplitResult(split_result.scheme, split_result.netloc, api_path, \
                                      urlencode(result_query), fragment) \
                                        .geturl()

            return urljoin(base_url, relative_url)

        except Exception as error:
            raise HttpUrlNotValid(error)
        
    def make_session_headers(self, session: HttpSession) -> dict:
        
        return session.make_headers(self.headers)

    @staticmethod
    def raise_on_4xx_5xx(response):
        response.raise_for_status()

# class AsyncWaitOn:

#     def __call__(func):
#         def decorator():
#             async def wrapper():
#                 try:
#                     app_promise = await PromisePool().the_promise("chanjet-tplus", "app_ticket", str(time()))
#                 except StopAsyncIteration as done:
#                     app_promise = done.value

#                 try:
#                     app_ticket_push = await app_promise
#                 except StopAsyncIteration as done:
#                     app_ticket_push = done.value
#             return wrapper            
#         return decorator
        

class Get(HttpMethods):

    def __init__(self, api_path: str, headers: dict = {}, cookies: HttpCookie = None, auth: object = None) -> None:
        super().__init__(api_path, headers = headers, cookies = cookies)


    def __call__(self, func):
        async def wrapper(http_call, *args, params = {}, fragment = "", urlargv = {}, **kwargs):

            session = http_call.http_session
            headers = self.make_session_headers(session)
            url_encoded = self.finalize_url(http_call.base_url, self.api_path, 
                                            params = params, fragment = fragment, 
                                            urlargv = urlargv)

            async with AsyncClient(event_hooks={'response': [HttpMethods.raise_on_4xx_5xx]}) as client:
                response = await client.get(url_encoded, params = params, 
                                            headers = headers, cookies = session.cookies,
                                            **kwargs)
                session.draw_cookie_update(response)

            return func(http_call, response)

        return wrapper


class Post(HttpMethods):

    def __init__(self, api_path: str, headers: dict = {}, cookies: HttpCookie = None, auth: object = None) -> None:
        super().__init__(api_path, headers = headers, cookies = cookies)

    def __call__(self, func):
        async def wrapper(http_call, *args, params = {}, fragment = "", urlargv = {}, **kwargs):

            session = http_call.http_session
            headers = self.make_session_headers(session)
            url_encoded = self.finalize_url(http_call.base_url, self.api_path, 
                                            params = params, fragment = fragment, 
                                            urlargv = urlargv)

            async with AsyncClient(event_hooks={'response': [HttpMethods.raise_on_4xx_5xx]}) as client:
                response = await client.get(url_encoded, params = params, 
                                            headers = headers, cookies = session.cookies,
                                            **kwargs)
                session.draw_cookie_update(response)

            return func(http_call, response)

        return wrapper
