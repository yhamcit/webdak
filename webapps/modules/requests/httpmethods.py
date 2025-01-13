
import functools

from types import FunctionType

from httpx import AsyncClient, ConnectTimeout, ReadTimeout

from urllib.parse import urlsplit
from urllib.parse import urlencode
from urllib.parse import parse_qs as urlsplit_qs
from urllib.parse import urljoin
from urllib.parse import SplitResult
from webapps.model.properties.dao.env_errors import ConfigContentError


from webapps.modules.requests.dao.http_errors import HttpInvalidUrl
from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.plugins.tplus.model.dao.tplus_errors import TplusException



_err_timber = Lumber.timber("error")

class HttpMethods(object):

    _API_PATH_  = 0
    _HEADERS_   = "headers"
    
    _HTTP_METHOD_CONNECT_   = 'CONNECT'
    _HTTP_METHOD_DELETE_    = 'DELETE'
    _HTTP_METHOD_GET_       = 'GET'
    _HTTP_METHOD_HEAD_      = 'HEAD'
    _HTTP_METHOD_OPTIONS_   = 'OPTIONS'
    _HTTP_METHOD_PATCH_     = 'PATCH'
    _HTTP_METHOD_POST_      = 'POST'
    _HTTP_METHOD_PUT_       = 'PUT'
    _HTTP_METHOD_TRACE_     = 'TRACE'

    _HTTP_METHODS_SET_ = set(
        {
            _HTTP_METHOD_CONNECT_, 
            _HTTP_METHOD_DELETE_, 
            _HTTP_METHOD_GET_, 
            _HTTP_METHOD_HEAD_, 
            _HTTP_METHOD_OPTIONS_, 
            _HTTP_METHOD_PATCH_, 
            _HTTP_METHOD_POST_, 
            _HTTP_METHOD_PUT_, 
            _HTTP_METHOD_TRACE_
        }
    )

    _timber = Lumber.timber("plugins")


    @staticmethod
    def determine_protocol_version(http_call: HttpCall, protocol):

        return (protocol == 'HTTP/2')

    @staticmethod
    def finalize_url(http_call: HttpCall, path_template, params= {}, fragment= "", argv: dict= {}) -> str:
        try:
            api_path = path_template.format(**argv)
            split_result = urlsplit(api_path)
            result_query = urlsplit_qs(split_result.query)

            if params:
                if not result_query:
                    result_query = list(params.items())
                else:
                    for key, value in result_query:
                        if key in params:
                            v = params[key]
                            value.extend(v) if isinstance(v, list) else value.append(v)
            
            relative_url = SplitResult(split_result.scheme, split_result.netloc, api_path, \
                                      urlencode(result_query), fragment) \
                                        .geturl()

            return urljoin(http_call.base_url, relative_url)

        except Exception as excp_err:
            raise HttpInvalidUrl(excp_err)
        
    @staticmethod
    def inflate_session_headers(http_call: HttpCall, header_filter: tuple, cust_headers: dict) -> dict:

        try:
            headers = http_call.http_session.supplement_headers(cust_headers)
            return dict({key: headers[key] for key in header_filter})
        except KeyError as excp_err:
            raise ConfigContentError(excp_err)


    @staticmethod
    async def call(http_call: HttpCall, method: str, http2: bool, url: str, headers: dict, func: FunctionType, **kwargs):
            
        session = http_call.http_session

        async with AsyncClient(http2=http2) as client:
            try:
                if http_call.http_interceptor:
                    http_call.http_interceptor(http_call, url, headers=headers, cookies=session, **kwargs)

                response = await client.request(method, url, headers =headers, cookies =session.cookies, **kwargs)

                if http_call.response_parser:
                    http_call.response_parser(http_call, response, headers=headers, session=session, **kwargs)

                return func(http_call, response, session)

            except TplusException as excp_err:
                HttpMethods._timber.critical(f"Unexpected exception: {str(excp_err)}")
            except ReadTimeout as excp_err:
                HttpMethods._timber.critical(f"Network timeout: {excp_err.request}")
            except ConnectTimeout as excp_err:
                HttpMethods._timber.critical(f"Connection timeout: {excp_err.request}")
            except Exception as excp_err:
                HttpMethods._timber.critical(f"Unexpected exception: {str(excp_err)}")

    @staticmethod
    def raise_on_4xx_5xx(response):
        response.raise_for_status()

    @staticmethod
    def REQUEST(call_path: str=None, 
                call_method: str = None, 
                header_filter:tuple =HttpHeaderPod._HTTP_DEFAULT_HEADERS_LIST_, 
                cust_headers: dict = HttpHeaderPod._HTTP_DEFAULT_HEADERS_, 
                protocol: str='HTTP/1.1'):

        def decorator(func):

            async def decroation(http_call: HttpCall, *args, url_params: dict= {}, url_fragments: str= "", url_argv: dict= {}, **kwargs):

                http_path  = call_path if call_path else http_call.api_path

                http_method = call_method if call_method else http_call.api_method
                assert http_method in HttpMethods._HTTP_METHODS_SET_

                url_encoded = HttpMethods.finalize_url(http_call, http_path, params =url_params,
                                                       fragment =url_fragments, argv =url_argv)
                http_call.api_path = url_encoded
                
                headers = HttpMethods.inflate_session_headers(http_call, header_filter, cust_headers)

                http2_enable = HttpMethods.determine_protocol_version(http_call, protocol)

                return await HttpMethods.call(http_call, http_method, http2_enable, url_encoded, headers, func, **kwargs)
            
            return decroation

        return decorator

    CONNECT = functools.partial(REQUEST, call_method =_HTTP_METHOD_CONNECT_)
    DELETE  = functools.partial(REQUEST, call_method =_HTTP_METHOD_DELETE_)
    GET     = functools.partial(REQUEST, call_method =_HTTP_METHOD_GET_)
    HEAD    = functools.partial(REQUEST, call_method =_HTTP_METHOD_HEAD_)
    OPTIONS = functools.partial(REQUEST, call_method =_HTTP_METHOD_OPTIONS_)
    PATCH   = functools.partial(REQUEST, call_method =_HTTP_METHOD_PATCH_)
    POST    = functools.partial(REQUEST, call_method =_HTTP_METHOD_POST_)
    PUT     = functools.partial(REQUEST, call_method =_HTTP_METHOD_PUT_)
    TRACE   = functools.partial(REQUEST, call_method =_HTTP_METHOD_TRACE_)