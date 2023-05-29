
import json
import base64

from Crypto.Cipher import AES
import httpx

from webapps.endpoints.tplus.auth.appticket import AppTicket
from webapps.model.actors.tplusappticketrepo import TplusAppTicketRepo
from webapps.model.properties.dao.actorenvironment import ActorsEnvironment
from webapps.model.properties.dao.tplusprofile import TplusOpenApiProfile

from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.httpcallrequests import HttpCallRequests
from webapps.modules.requests.httpcall import HttpCall

from webapps.language.decorators.singleton import singleton

from webapps.modules.requests.httpmethods import Post
from webapps.modules.requests.httpresponse import HttpResponseParser


__timber = Lumber.timber("actors")


@singleton
class AppTicketActor(object):

    __SUCCESS__ = {"result": "success"}

    __FAILURE__ = {"result": "failed"}

    __ACTOR_PROFILE__ = ActorsEnvironment() \
                        .get_actor_profile(
                            ActorsEnvironment.make_identifier(__module__, "AppTicketActor"))

    def __init__(self, actor_profile) -> None:
        self._app_ticket_repo = TplusAppTicketRepo()
        self._actor_profile = actor_profile
        self._http_call_builder = HttpCallRequests() \
                                    .set_base_url(self.actor_profile.base_url) \
                                    .make_builder()
        
    async def renew_app_token(self):
        __timber = Lumber.timber("renew_app_token")

        http_call = self.http_call_builder.build(TplusHttpCall)
        
        result = await http_call.refresh_app_ticket()

        if result:
            return "OK!"

    async def exchange_app_ticket(self):
        __timber = Lumber.timber("exchange_app_ticket")
        http_call = self.http_call_builder.build(TplusHttpCall)

        certificate = AppTicketActor.__ACTOR_PROFILE__.app_token_certifcate

        json_params = {
            TplusOpenApiProfile.__APP_TICKET__: self.app_ticket, 
            TplusOpenApiProfile.__CERTIFICATE__: certificate
        }

        return await http_call.exchange_app_token(json = json_params)

    @staticmethod
    def success():
        __timber = Lumber.timber("staticmethod.success()")
        return json.dumps(AppTicketActor.__SUCCESS__)

    @staticmethod
    def failure():
        __timber = Lumber.timber("staticmethod.failure()")
        return json.dumps(AppTicketActor.__FAILURE__)

    @property
    def actor_profile(self):
        return self._actor_profile

    @actor_profile.setter
    def actor_profile(self, actor_profile):
        self._actor_profile = actor_profile

    @property
    def app_ticket(self):
        return self._app_ticket_repo.ticket

    @app_ticket.setter
    def app_ticket(self, app_ticket):
        self._app_ticket_repo.ticket = app_ticket

    @property
    def http_call_builder(self):
        return self._http_call_builder

    @http_call_builder.setter
    def http_call_builder(self, http_call_builder):
        self._http_call_builder = http_call_builder

    def resolve_ticket(self, content: str):
        # TODO: exception
        infomation = self.decrypt_push_message(content)

        return AppTicket(infomation)

    def decrypt_push_message(self, content) -> str:

        decrypt_key = self.actor_profile.cipher_key.encode("utf8")
        cipher = AES.new(decrypt_key, AES.MODE_ECB)

        ciphertext = content[TplusOpenApiProfile.__ENCRYPT_MSG__]
        cipherbytes = bytes(ciphertext, encoding='utf8')
        raw_text = cipher.decrypt(base64.decodebytes(cipherbytes))
        infomation = raw_text.decode("utf8")

        return json.loads(infomation)


class TplusHttpCall(HttpCall):

    # __ACTOR_PROFILE__ = ActorsEnvironment() \
    #                     .get_actor_profile(
    #                         ActorsEnvironment.make_identifier(__module__, "AppTicketActor"))

    __BASE_URL__    = AppTicketActor.__ACTOR_PROFILE__.base_url
    __APP_KEY__     = AppTicketActor.__ACTOR_PROFILE__.app_key
    __APP_SECRET__  = AppTicketActor.__ACTOR_PROFILE__.app_secret
    __CERTIFICATE__ = AppTicketActor.__ACTOR_PROFILE__.app_token_certifcate
    __TICKET_PATH__ = AppTicketActor.__ACTOR_PROFILE__.app_ticket_api_path
    __TOKEN_PATH__  = AppTicketActor.__ACTOR_PROFILE__.app_token_api_path

    @Post(__TICKET_PATH__, headers =
         {
            TplusOpenApiProfile.__APP_KEY__: __APP_KEY__,
            TplusOpenApiProfile.__APP_SECRET__: __APP_SECRET__,
         })
    def refresh_app_ticket(self, response: HttpResponseParser):

        if response.status_code != httpx.codes.OK:
            return False
        
        return True
        

    @Post(__TOKEN_PATH__, headers =
         {
            TplusOpenApiProfile.__APP_KEY__: __APP_KEY__,
            TplusOpenApiProfile.__APP_SECRET__: __APP_SECRET__,
            "Content-Type": "application/json"
         })
    def exchange_app_token(self, response: HttpResponseParser):
        return True
