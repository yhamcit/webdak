
from typing import Any
import httpx
import json
import base64

from quart import ResponseReturnValue, request
from quart.views import MethodView

from Cryptodome.Util.Padding import unpad
from Cryptodome.Cipher import AES
from webapps.modules.requests.dao.http_errors import HttpRequestReject

from webapps.language.decorators.singleton import Singleton
from webapps.modules.plugin.endpoints import PluginEndpoint

from webapps.plugins.tplus.model.auth.app_ticket import AppTicket

from webapps.model.auth.access.tic_tok_depot import SerializableObjectDepot
from webapps.plugins.tplus.model.properties.tplus_endpoint_profile import TplusEndpointProfile
from webapps.plugins.tplus.model.properties.tplus_openapi_properties import TplusOpenApiProperties
from webapps.model.identifier import ModelIdentifier
from webapps.modules.coroutinpromise.promisepool import PromisePool

from webapps.modules.lumber.lumber import Lumber
from webapps.plugins.tplus.core import TplusPlugin



@Singleton
class AppTicketEndpoints(PluginEndpoint):

    _ID_                = "id"
    _APP_KEY_           = "appKey"
    _MSG_TYPE_          = "msgType"
    _TIME_              = "time"
    _BIZ_CONTENT_       = "bizContent"

    _ENCRYPT_MSG_       = "encryptMsg"

    _APP_TEST_MSG_      = "APP_TEST"
    _APP_TICKET_MSG_    = "APP_TICKET"
    _TEMP_AUTH_CODE_    = "TEMP_AUTH_CODE"

    _timber = Lumber.timber("endpoints")


    class View(MethodView):

        def __init__(self, endpoint: PluginEndpoint) -> None:
            super().__init__()
            self._endpoint = endpoint

        async def post(self, **kwargs: Any) -> ResponseReturnValue:
            cipher_msg = await request.get_json()
            valueset = AppTicketEndpoints().decrypt_msg(cipher_msg)

            AppTicketEndpoints._timber.debug(valueset)

            if valueset:
                if AppTicketEndpoints._MSG_TYPE_ in valueset:
                    msg_type = valueset[AppTicketEndpoints._MSG_TYPE_]

                    if msg_type == AppTicketEndpoints._APP_TEST_MSG_:
                        return TplusPlugin.success()
                    
                    elif msg_type == AppTicketEndpoints._APP_TICKET_MSG_:
                        ticket = AppTicket(valueset)
                        self._endpoint.put_app_ticket(ticket)
                        AppTicketEndpoints._timber.info(f"Get pushed ticket: {ticket.ticket}, at time: {ticket.timestamp}")

                        PromisePool.promise(self._endpoint.identifier, ticket)

                        return TplusPlugin.success()
                    elif msg_type == AppTicketEndpoints._TEMP_AUTH_CODE_:
                        # 获取企业永久授权码
                        # POST : /auth/orgAuth/getPermanentAuthCode
                        # {
                        #     "appAccessToken":"909c1237a7cd4858a8a825afda7924bb",
                        #     "tempAuthCode":"961b21d4e65b4981939f2bca7fcf012b"
                        # }
                        return json.dumps(valueset)
                    else:
                        AppTicketEndpoints._timber.info(f"handle_msg() got _MSG_TYPE_: others")
                        return TplusPlugin.failure()
            
            raise HttpRequestReject(AppTicketEndpoints._FAIL_RSP_)


    def __init__(self, name: str, profile: TplusEndpointProfile, props: TplusOpenApiProperties) -> None:
        super().__init__(name, profile)

        self._name = name
        self._profile = profile
        self._properties = props

        self._app_ticket_repo = SerializableObjectDepot()

        self._http_envalue_set = {**props.valueset, **profile.valueset}
        self._identifier = ModelIdentifier(props.plugin_qualifier, profile.endpoint_qualifier, self.url)

        PromisePool.subscribe_channel((self._identifier, ))
    
    @property
    def view(self):
        return AppTicketEndpoints.View.as_view("tplus_ticket", self)

    @property
    def identifier(self):
        return self._identifier

    @property
    def http_envalue_set(self):
        return self._http_envalue_set
    
    def put_app_ticket(self, ticket: AppTicket):
        self._app_ticket_repo.put(ticket, self._identifier)

    def decrypt_msg(self, content: str) -> dict:
        infomation = self.decrypt_push_message(content)

        AppTicketEndpoints._timber.debug(f"AppTicketActuator.decrypt_msg() - ticket: {infomation}")

        return infomation

    def decrypt_push_message(self, content) -> dict:

        decrypt_key = self._properties.cipher_key.encode("utf8")
        cipher = AES.new(decrypt_key, AES.MODE_ECB)

        ciphertext = content[AppTicketEndpoints._ENCRYPT_MSG_]
        cipherbytes = bytes(ciphertext, encoding='utf8')
        raw_text = unpad(cipher.decrypt(base64.decodebytes(cipherbytes)), 16)
        infomation = raw_text.decode("utf8")

        return json.loads(infomation)

    @staticmethod
    def query_subscription() -> ModelIdentifier:
        try:
            return AppTicketEndpoints().identifier
        except Exception as error:
            AppTicketEndpoints._timber.critical("AppTicketEndpoints invoked before it is created.")


