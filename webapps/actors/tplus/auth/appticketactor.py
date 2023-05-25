
import json
import base64

from Crypto.Cipher import AES

from webapps.endpoints.tplus.auth.appticket import AppTicket
from webapps.language.errors.tpluserror import AppTicketExpired
from webapps.model.properties.dao.actorenvironment import ActorsEnvironment
from webapps.model.properties.dao.tplusprofile import TplusOpenApiProfile
from webapps.modules.asyncoroutine.promisepool import PromisePool
from webapps.modules.requests.httpcallrequests import HttpCallRequests
from webapps.modules.requests.httpcall import HttpCall

from webapps.language.decorators.singleton import singleton

from webapps.modules.requests.httpmethods import Get
from webapps.modules.requests.httpmethods import Post
from webapps.modules.requests.httpresponse import HttpResponseParser


@singleton
class AppTicketActor(object):

    __SUCCEED__ = {"result": "success"}

    __FAILURE__ = {"result": "failed"}

    def __init__(self, actor_profile) -> None:
        self._app_ticket_repo = None
        self._actor_profile = actor_profile
        self._http_call_builder = HttpCallRequests() \
                                    .set_base_url(self.actor_profile.base_url) \
                                    .make_builder()
        
    async def exchange_app_token(self):
        http_call = self.http_call_builder.build(TplusHttpCall)
        try:
            return await http_call.exchange_app_token(self.app_ticket)
        except AppTicketExpired as error:
            return await self.renew_app_token()

    async def renew_app_token(self):
        http_call = self.http_call_builder.build(TplusHttpCall)
        
        result = await http_call.refresh_app_ticket()

        if not result:
            pass

        the_promise = await PromisePool().the_promise()

        await the_promise

        return await http_call.exchange_app_token(self.app_ticket)

    @staticmethod
    def succeed():
        return json.dumps(AppTicketActor.__SUCCEED__)

    @staticmethod
    def failure():
        return json.dumps(AppTicketActor.__FAILURE__)

    @property
    def actor_profile(self):
        return self._actor_profile

    @actor_profile.setter
    def actor_profile(self, actor_profile):
        self._actor_profile = actor_profile

    @property
    def app_ticket(self):
        return self._app_ticket_repo.app_ticket

    @app_ticket.setter
    def app_ticket(self, app_ticket):
        self._app_ticket_repo.app_ticket = app_ticket

    @property
    def http_call_builder(self):
        return self._http_call_builder

    @http_call_builder.setter
    def http_call_builder(self, http_call_builder):
        self._http_call_builder = http_call_builder

    def decrypt_push_message(self, content) -> str:

        decrypt_key = self.actor_profile.cipher_key.encode("utf8")
        cipher = AES.new(decrypt_key, AES.MODE_ECB)

        ciphertext = content[TplusOpenApiProfile.__ENCRYPT_MSG__]
        cipherbytes = bytes(ciphertext, encoding='utf8')
        raw_text = cipher.decrypt(base64.decodebytes(cipherbytes))
        infomation = raw_text.decode("utf8")

        return json.loads(infomation)


        """
        
        "AES/ECB/PKCS5Padding"

        {
        "encryptMsg":"E4M54v2CbwnbdG+quqWwgFGI5dgx3shx2gGZRiihvkQQLgbH12Y9/dJXO1/7H7QLL3H9fstismlYMLQrZxShEyknFJcLG96HbG4Cx/7gq4YMXgZJDI9Qvm1sH6H4arIHaPTSbHTk

        faYo7fo6Sc3lwBMOpJHi33Os5u7DobPmqkzkuyoRxbTD4mZaSYleDcYuouQTdma+rubH5PPzg0+R09XsEHWkgF6cc+Ylh2w0N6590eJDNdQvoI4m7eSiWQCJo5nN5zXj/2QeQcYwIfdpmQ=="

        }

        {
            "id":"85668539-205a-05cc-60ae-6ed642d8227d",  //消息ID
            "appKey":"mMQVm4Az",   //开放平台appKey
            "msgType":"APP_TICKET", //消息类型
            "time":"1603856412356", //时间戳
            "bizContent":{
                "appTicket":"6366841b552340e4b65162d09cf88278"   //appTicket
            }
        }

        """


class TplusHttpCall(HttpCall):

    __ACTOR_PROFILE__ = ActorsEnvironment() \
                        .get_actor_profile(
                            ActorsEnvironment.make_identifier(__module__, "AppTicketActor"))

    __BASE_URL__    = __ACTOR_PROFILE__.base_url
    __APP_KEY__     = __ACTOR_PROFILE__.app_key
    __APP_SECRET__  = __ACTOR_PROFILE__.app_secret
    __CERTIFICATE__ = __ACTOR_PROFILE__.app_token_certifcate
    __TICKET_PATH__ = __ACTOR_PROFILE__.app_ticket_api_path
    __TOKEN_PATH__  = __ACTOR_PROFILE__.app_token_api_path

    @Post(__TICKET_PATH__, headers =
         {
            TplusOpenApiProfile.__APP_KEY__: __APP_KEY__,
            TplusOpenApiProfile.__APP_SECRET__: __APP_SECRET__,
         })
    def refresh_app_ticket(self, response: HttpResponseParser):
        pass

    @Post(__TOKEN_PATH__, headers =
         {
            TplusOpenApiProfile.__APP_KEY__: __APP_KEY__,
            TplusOpenApiProfile.__APP_SECRET__: __APP_SECRET__,
         })
    def exchange_app_token(self, response: HttpResponseParser):
        pass
