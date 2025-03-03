
import json
import httpx
import gzip

from webapps.modules.lumber.lumber import Lumber

from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.modules.requests.httpmethods import HttpMethods
from webapps.modules.requests.httpsession import HttpSession
from webapps.plugins.cbs.errors.cbs_error import ServerRejection, UpstreamServiceError


class CBSOpenapiBrokerHttpCall(HttpCall):

    _timber                 = Lumber.timber("endpoints")
    _err_timber             = Lumber.timber("error")

    _HDR_AUTHORIZATION_         = "Authorization"
    _HDR_X_MBCLOUD_API_SIGN_    = "X-MBCLOUD-API-SIGN"

    _HDR_X_MBCLOUD_TIMESTAMP_   = "X-MBCLOUD-TIMESTAMP"

    _ARGKEY_GRANT_TYPE_         = "grant_type"
    _ARGVAL_CLIENT_CREDENTIALS_ = "client_credentials"

    _X_MBCLOUD_ENCRYPTION_EN_   = "X-MBCLOUD-ENCRYPTION-ENABLED"
    _X_MBCLOUD_ENCRYPTION_TRUE_ = "true"

    _X_MBCLOUD_COMPRESSION_EN_  = "X-MBCLOUD-COMPRESS"
    _X_MBCLOUD_COMPRESS_TRUE_   = "true"



    __refresh_token_headdr_filter = HttpHeaderPod._HTTP_DEFAULT_HEADERS_LIST_ + (
        HttpHeaderPod._HDR_CONTENT_TYPE_, 
        _HDR_AUTHORIZATION_,
    )
    __broker_api_headdr_filter = (
        HttpHeaderPod._HDR_CONTENT_TYPE_, 
        _HDR_AUTHORIZATION_,
        _HDR_X_MBCLOUD_API_SIGN_,
        _HDR_X_MBCLOUD_TIMESTAMP_,
    )
    __broker_api_cust_headers = HttpHeaderPod._HTTP_DEFAULT_HEADERS_ | {
        HttpHeaderPod._HDR_CONTENT_TYPE_: HttpHeaderPod._HDV_MIME_JSON_
    }

    @HttpMethods.POST(call_path="/openapi/app/v1/app/token", cust_headers =__broker_api_cust_headers)
    def require_token(self, response: httpx.Response, session: HttpSession):
        CBSOpenapiBrokerHttpCall._timber.debug("CBSOpenapiBrokerHttpCall.require_token()")
        
        if response.status_code != httpx.codes.OK:
            raise ServerRejection("Server reject this request, checked Certificates?")
       
        try:
            CBSOpenapiBrokerHttpCall._timber.debug(f"get exchanged token: {response.text}")
            return response.json()
        except Exception as error:
            CBSOpenapiBrokerHttpCall._timber.debug(f"Error: {error}; Remote server reject because of: {response.text}")
            raise UpstreamServiceError(error)



    @HttpMethods.GET(call_path="/openapi/app/v1/app/refresh-token", header_filter =__refresh_token_headdr_filter, cust_headers =__broker_api_cust_headers)
    def refresh_token(self, response: httpx.Response, session: HttpSession):
        CBSOpenapiBrokerHttpCall._timber.debug("CBSOpenapiBrokerHttpCall.refresh_token()")
        
        if response.status_code != httpx.codes.OK:
            raise ServerRejection("Server reject this request, checked Certificates?")
       
        try:
            CBSOpenapiBrokerHttpCall._timber.debug(f"get exchanged token: {response.text}")
            return response.json()
        except Exception as error:
            CBSOpenapiBrokerHttpCall._timber.debug(f"Error: {error}; Remote server reject because of: {response.text}")
            raise UpstreamServiceError(error)


    @HttpMethods.REQUEST(header_filter =__broker_api_headdr_filter, cust_headers =__broker_api_cust_headers)
    def broker_api_call(self, response: httpx.Response, session: HttpSession):
        CBSOpenapiBrokerHttpCall._timber.debug("CBSOpenapiBrokerHttpCall.broker_api()")

        try:
            if response.status_code != httpx.codes.OK:
                CBSOpenapiBrokerHttpCall._timber.error(f"Upstream server rejection: status code: {response.status_code} response details: \n {response.text}")

            # session.headers.update(headers=headers)

            headers = HttpHeaderPod(defaults=response.headers)
            if headers.test(CBSOpenapiBrokerHttpCall._X_MBCLOUD_COMPRESSION_EN_, CBSOpenapiBrokerHttpCall._X_MBCLOUD_COMPRESS_TRUE_):
                self.response = gzip.decompress(self.response)

            return self.response.decode('utf-8')

        except Exception as error:
            CBSOpenapiBrokerHttpCall._timber.error(f"CBSOpenapiBrokerHttpCall: {error}")
            CBSOpenapiBrokerHttpCall._timber.error(f"CBSOpenapiBrokerHttpCall reason: {error.args}")

            # In case of upstream exception, return a error
            return json.dumps({"Result": f"Upstream server report an error: {error.args}"}), 505
