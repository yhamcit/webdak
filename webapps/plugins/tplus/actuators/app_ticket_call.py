
import httpx
from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.httpheaderpod import HttpHeaderPod

from webapps.modules.requests.httpmethods import HttpMethods

from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpsession import HttpSession

from webapps.plugins.tplus.model.dao.tplus_errors import AppTicketRequestReject
from webapps.plugins.tplus.model.properties.tplus_openapi_properties import TplusOpenApiProperties


class TplusTicketHttpCall(HttpCall):

    _timber         = Lumber.timber("endpoints")
    _err_timber     = Lumber.timber("error")

    __refresh_ticket_header_filter = HttpHeaderPod._HTTP_DEFAULT_HEADERS_LIST_ + (
        TplusOpenApiProperties._APP_KEY_, TplusOpenApiProperties._APP_SECRET_
    )

    __refresh_ticket_cust_headers = HttpHeaderPod._HTTP_DEFAULT_HEADERS_ | {
        HttpHeaderPod._HDR_CONTENT_TYPE_: HttpHeaderPod._HDV_MIME_JSON_
    }

    @HttpMethods.POST(call_path= "/auth/appTicket/resend", header_filter =__refresh_ticket_header_filter, cust_headers =HttpHeaderPod._HTTP_DEFAULT_HEADERS_)
    def refresh_app_ticket(self, response: httpx.Response, session: HttpSession):
        TplusTicketHttpCall._timber.debug("TplusHttpCall.refresh_app_ticket()")

        if response.status_code != httpx.codes.OK:
            raise AppTicketRequestReject("Server rejected the request, check AppKey\AppSecrect. Doese target company match request?")
        
        return "Success", 200
