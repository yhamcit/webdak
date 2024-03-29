
import traceback
from typing import Any


from quart import ResponseReturnValue, request as view_request
from quart.views import View

from webapps.language.decorators.singleton import Singleton

from webapps.model.auth.access.access_errors import SerializableObjectNotAvialable
from webapps.model.identifier import ModelIdentifier
from webapps.model.auth.access.tic_tok_depot import SerializableObjectDepot
from webapps.modules.coroutinpromise.promisepool import PromisePool

from webapps.modules.lumber.lumber import Lumber

from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.modules.requests.httpcallbuilder import HttpCallBuilder
from webapps.modules.requests.httpheaders import HttpHeaders

from webapps.plugins.tplus.actuators.api_broker_call import TplusOpenapiBrokerHttpCall
from webapps.plugins.tplus.actuators.app_ticket_call import TplusTicketHttpCall
from webapps.plugins.tplus.actuators.app_token_call import TplusAppTokenHttpCall
from webapps.plugins.tplus.endpoints.auth.ticket import AppTicketEndpoints

from webapps.plugins.tplus.model.auth.app_ticket import AppTicket
from webapps.plugins.tplus.model.auth.app_token import AppToken
from webapps.plugins.tplus.model.dao.api_broker_request import TplusRestfulapiBrokerRequest
from webapps.plugins.tplus.model.dao.tplus_errors import AppTicketExpired, AppTokenExpired, AppTokenInvalid
from webapps.plugins.tplus.model.properties.tplus_endpoint_profile import TplusEndpointProfile
from webapps.plugins.tplus.model.properties.tplus_openapi_properties import TplusOpenApiProperties





@Singleton
class TplusOpenapiBroker(PluginEndpoint):

    _timber = Lumber.timber("endpoints")
    _err_timber = Lumber.timber("error")

    _ARGKEY_GRANT_TYPE_    = "grantType"
    _ARGVLU_REFRESH_TOKEN_ = "refresh_token"

    _ARGKEY_REFRESH_TOKEN_ = "refreshToken"

    class BrokerView(View):

        methods = ["GET", "POST"]

        def __init__(self, endpoint: PluginEndpoint) -> None:
            super().__init__()
            self._endpoint = endpoint

        async def dispatch_request(self, **kwargs: Any) -> ResponseReturnValue:

            if not TplusRestfulapiBrokerRequest._REQUEST_HEADER_CONTENT_TYPE_ in view_request.headers:
                return "A valid request must contain specified: 'Content-Type' as 'application/json'."

            content_type = view_request.headers.get(TplusRestfulapiBrokerRequest._REQUEST_HEADER_CONTENT_TYPE_)
            if (content_type != HttpHeaders._HDV_MIME_JSON_):
                return 'Content-Type not supported!'

            request = TplusRestfulapiBrokerRequest(await view_request.get_json())
            try:
                return await self._endpoint.request(request.api_path, request.api_method, request.body)
            except Exception as error:
                TplusOpenapiBroker._err_timber.error(f"{error}")
                TplusOpenapiBroker._err_timber.error(f"{error.args}")

                return "Request data is invalid/malformatted", 404


    def __init__(self, name: str, profile: TplusEndpointProfile, props: TplusOpenApiProperties) -> None:
        super().__init__(name, profile)

        assert profile and props

        self._profile = profile
        self._props = props

        self._conf_vault = dict(profile.valueset | props.valueset)

        self._seri_obj_depot = SerializableObjectDepot()
        self._http_call_builder = HttpCallBuilder(props.base_url)

        self._tok_identifier = ModelIdentifier(props.plugin_qualifier, profile.endpoint_qualifier, self.url)
        self._tic_identifier = AppTicketEndpoints.query_subscription()

        header_dic = {
            TplusOpenApiProperties._APP_KEY_: props.app_key,
            TplusOpenApiProperties._APP_SECRET_: props.app_secret
        }
        self._http_call_builder.headers = HttpHeaders(defaults =header_dic)

        
    def get_app_ticket(self) -> AppTicket:
        app_tic = AppTicket(self._seri_obj_depot.get(self._tic_identifier))

        if not app_tic.is_valid:
            raise AppTicketExpired(f"{app_tic.ticket} has expired. Lifetime: {app_tic.lifetime}.")
        
        return app_tic

    def get_token(self) -> AppToken:
        app_tok = AppToken(self._seri_obj_depot.get(self._tok_identifier))

        if not app_tok.is_valid:
            if not app_tok.is_expired:
                raise AppTokenInvalid(f"{app_tok.access_token_lifetime}")
            else:
                raise AppTicketExpired(f"{app_tok.refresh_token_lifetime}")
        
        return app_tok
        
    def put_token(self, app_tok) -> None:
        self._seri_obj_depot.put(app_tok, self._tok_identifier)

    async def try_fetch_ticket(self) -> AppTicket:
        ticket = None
        try:
            ticket = self.get_app_ticket()
        except (SerializableObjectNotAvialable, AppTicketExpired) as error:
            TplusOpenapiBroker._timber.info(f"App Ticket Error - not avialable or expired: '{error}', RENEWING.")
            ticket = await self.renew_app_ticket()
        finally:
            return ticket

    async def try_fetch_token(self) -> AppToken:
        token = None
        try:
            token = self.get_token()
        except (SerializableObjectNotAvialable, AppTokenExpired, AppTokenInvalid) as error:
            TplusOpenapiBroker._timber.info(f"App Token not avialable or expired: '{error}', RENEWING needed.")

            ticket = await self.try_fetch_ticket()
            token = await self.exchange_for_token(ticket)
            self.put_token(token)
        finally:
            return token

    async def renew_app_ticket(self):
        TplusOpenapiBroker._timber.debug(f"Calling renew_app_ticket()")

        http_call = self._http_call_builder.build(TplusTicketHttpCall, self._conf_vault)

        try:
            await http_call.refresh_app_ticket()
            app_tic = await PromisePool.wish(self._tic_identifier, None)
        except Exception as error:
            TplusOpenapiBroker._err_timber.error(f"Skipped waiting for app-ticket promise because: {error} - {error.args}")
            raise(error)

        return app_tic

    async def exchange_for_token(self, app_tic: AppTicket =None):
        TplusOpenapiBroker._timber.debug("Calling exchange_for_token()")

        http_call = self._http_call_builder.build(TplusAppTokenHttpCall, self._conf_vault)

        exchange_params = {
            TplusEndpointProfile._APP_TICKET_: app_tic.ticket,
            TplusOpenApiProperties._CERTIFICATE_: self._props.certificate
        }

        token_txt = await http_call.exchange_app_token(json = exchange_params)
        return AppToken(token_txt)


    async def refresh_token(self, app_tok: AppToken):
        TplusOpenapiBroker._timber.debug("Calling refresh_token()")

        refresh_params = {
            TplusOpenapiBroker._ARGKEY_GRANT_TYPE_: TplusOpenapiBroker._ARGVLU_REFRESH_TOKEN_,
            TplusOpenapiBroker._ARGKEY_REFRESH_TOKEN_: app_tok.refresh_token
        }

        http_call = self._http_call_builder.build(TplusAppTokenHttpCall, self._conf_vault)

        token_json = await http_call.refresh_app_token(url_params =refresh_params)
        return AppToken(token_json)


    async def request(self, api_path: str, api_method: str, request_body: dict):

        app_token = await self.try_fetch_token()
        headers = HttpHeaders(defaults={TplusOpenapiBrokerHttpCall._HDR_APP_TOKEN_: app_token.access_token})

        http_call = self._http_call_builder.build(TplusOpenapiBrokerHttpCall, self._conf_vault, api_path =api_path, api_method =api_method)
        http_call.update_http_headers(headers)

        return await http_call.broker_api_call(api_path, api_method, json =request_body)


    @property
    def view(self):
        return TplusOpenapiBroker.BrokerView.as_view(self._profile.name, self)
    
