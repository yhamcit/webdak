

import httpx

from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.dao.http_errors import HttpServerReject
from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.modules.requests.httpmethods import HttpMethods
from webapps.modules.requests.httpsession import HttpSession
from webapps.plugins.tplus.model.dao.tplus_errors import AppTicketRejectedByServer
from webapps.plugins.tplus.model.properties.tplus_openapi_properties import TplusOpenApiProperties


class TplusAppTokenHttpCall(HttpCall):

    _timber         = Lumber.timber("endpoints")
    _err_timber     = Lumber.timber("error")

    __exchange_token_header_filter = HttpHeaderPod._HTTP_DEFAULT_HEADERS_LIST_ + (
        HttpHeaderPod._HDR_CONTENT_TYPE_, 
        TplusOpenApiProperties._APP_KEY_, 
        TplusOpenApiProperties._APP_SECRET_
    )
    __exchange_token_cust_headers = HttpHeaderPod._HTTP_DEFAULT_HEADERS_ | {
        HttpHeaderPod._HDR_CONTENT_TYPE_: HttpHeaderPod._HDV_MIME_JSON_
    }

    @HttpMethods.POST(call_path= "/v1/common/auth/selfBuiltApp/generateToken", header_filter =__exchange_token_header_filter, cust_headers =__exchange_token_cust_headers)
    def exchange_app_token(self, response: httpx.Response, session: HttpSession):
        TplusAppTokenHttpCall._timber.debug("TplusAppTokenHttpCall.exchange_app_token()")
        
        if response.status_code != httpx.codes.OK:
            raise AppTicketRejectedByServer("App ticket rejected by server. Checked Certificates?")
       
        try:
            TplusAppTokenHttpCall._timber.debug(f"get exchanged token: {response.text}")

            return response.json()
        except Exception as error:
            TplusAppTokenHttpCall._timber.debug(f"Error: {error}; Remote server reject because of: {response.text}")
            raise HttpServerReject(error)


    @HttpMethods.GET(call_path= "/auth/v2/refreshToken", header_filter =__exchange_token_header_filter, cust_headers =__exchange_token_cust_headers)
    def refresh_app_token(self, response: httpx.Response, session: HttpSession):
        TplusAppTokenHttpCall._timber.debug("TplusAppTokenHttpCall.refresh_app_token()")
        
        if response.status_code != httpx.codes.OK:
            raise AppTicketRejectedByServer("App ticket rejected by server. Checked Certificates?")
       
        try:
            TplusAppTokenHttpCall._timber.debug(f"get exchanged token: {response.text}")
            
            return response.json()
        except Exception as error:
            TplusAppTokenHttpCall._timber.debug(f"Error: {error}; Remote server reject because of: {response.text}")
            raise HttpServerReject(error)
 
