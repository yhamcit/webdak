import httpx
import json


from quart import request
from webapps.modules.plugin.endpoints import PluginEndpoint

from webapps.modules.plugin.plugin_blueprint import PluginBlueprint
from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.modules.requests.httpsession import HttpSession
from webapps.plugins.tplus.endpoints.auth.ticket import AppTicketEndpoints

from webapps.model.auth.access.tic_tok_depot import SerializableObjectDepot
from webapps.model.identifier import ModelIdentifier

from webapps.plugins.tplus.model.auth.app_ticket import AppTicket
from webapps.plugins.tplus.model.auth.app_token import AppToken
from webapps.plugins.tplus.model.dao.tplus_errors import AppTicketExpired, AppTicketRejectedByServer, AppTicketRequestReject
from webapps.plugins.tplus.model.properties.tplus_openapi_properties import TplusOpenApiProperties

from webapps.modules.requests.dao.http_errors import HttpServerReject
from webapps.modules.coroutinpromise.promisepool import PromisePool

from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.httpcall import HttpCall

from webapps.modules.requests.httpmethods import HttpMethods




class TplusOpenapiBrokerHttpCall(HttpCall):

    _timber                     = Lumber.timber("endpoints")
    _err_timber                 = Lumber.timber("error")

    _HDR_APP_TOKEN_             = "openToken"

    __broker_api_header_filter = HttpHeaderPod._HTTP_DEFAULT_HEADERS_LIST_ + (
        HttpHeaderPod._HDR_CONTENT_TYPE_, 
        TplusOpenApiProperties._APP_KEY_,
        TplusOpenApiProperties._APP_SECRET_,
        _HDR_APP_TOKEN_
    )
    __broker_api_cust_headers  = HttpHeaderPod._HTTP_DEFAULT_HEADERS_ | {
        HttpHeaderPod._HDR_CONTENT_TYPE_: HttpHeaderPod._HDV_MIME_JSON_
    }


    @HttpMethods.REQUEST(header_filter =__broker_api_header_filter, cust_headers =__broker_api_cust_headers)
    def broker_api_call(self, response: httpx.Response, session: HttpSession):
        TplusOpenapiBrokerHttpCall._timber.debug("TplusOpenapiBrokerHttpCall.broker_post()")
        
        try:
            if response.status_code != httpx.codes.OK:
                TplusOpenapiBrokerHttpCall._timber.error(f"Upstream server rejection: status code: {response.status_code} response details: \n {response.text}")

            return response.text, response.status_code
        except Exception as error:
            TplusOpenapiBrokerHttpCall._timber.error(f"TplusOpenapiBrokerHttpCall: {error}")
            TplusOpenapiBrokerHttpCall._timber.error(f"TplusOpenapiBrokerHttpCall reason: {error.args}")

            # In case of upstream exception, return a error
            return json.dumps({"Result": f"Upstream server report an error: {error.args}"}), 505
 