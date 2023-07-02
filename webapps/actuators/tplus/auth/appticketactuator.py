
import json
import base64

from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES


import httpx

from webapps.endpoints.tplus.auth.appticket import AppTicket
from webapps.endpoints.tplus.auth.apptoken import AppToken
from webapps.language.errors.tpluserror import AppTicketRejectedByServer, AppTicketRequestReject
from webapps.model.actuators.tplusappticketrepo import TplusAppTicketRepo
from webapps.model.properties.dao.actorenvironment import actuatorsEnvironment
from webapps.model.properties.dao.tplusprofile import TplusOpenApiProfile

from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.httpcallrequests import HttpCallRequests
from webapps.modules.requests.httpcall import HttpCall

from webapps.language.decorators.singleton import singleton

from webapps.modules.requests.httpmethods import Post



@singleton
class AppTicketActuator(object):

    _timber = Lumber.timber("actuators")

    _app_id_ = "86816166-240D-46D8-9BDD-CDE315D84DF0"

    __SUCCESS__ = {"result": "success"}

    __FAILURE__ = {"result": "failed"}
    
    __ENCRYPT_MSG__ = "encryptMsg"

    __ACTOR_PROFILE__ = actuatorsEnvironment() \
                        .get_actor_profile(
                            actuatorsEnvironment.make_identifier(__module__, "AppTicketActuator"))

    def __init__(self, actor_profile) -> None:
        self._app_ticket_repo = TplusAppTicketRepo()
        self._actor_profile = actor_profile
        self._http_call_builder = HttpCallRequests() \
                                    .set_base_url(self.actor_profile.base_url) \
                                    .make_builder()
        
    async def renew_app_token(self):
        AppTicketActuator._timber.debug("renew_app_token")

        http_call = self.http_call_builder.build(TplusHttpCall)
        
        await http_call.refresh_app_ticket()

    async def exchange_app_ticket(self, app_ticket: AppTicket = None):
        AppTicketActuator._timber.debug("exchange_app_ticket")

        http_call = self.http_call_builder.build(TplusHttpCall)

        certificate = AppTicketActuator.__ACTOR_PROFILE__.app_token_certifcate

        ticket = self.app_ticket.ticket if app_ticket is None else app_ticket.ticket

        json_params = {
            TplusOpenApiProfile.__APP_TICKET__: ticket,
            TplusOpenApiProfile.__CERTIFICATE__: certificate
        }

        return await http_call.exchange_app_token(json = json_params)
    
    @staticmethod
    def ed25519_sign_verify():
        from Crypto.PublicKey import ECC
        from Crypto.Signature import eddsa
        from Crypto.Hash import SHA512

        _ed25519_key_private_ = b"""-----BEGIN OPENSSH PRIVATE KEY-----
        b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
        QyNTUxOQAAACAjyTJVHi3HRj31IDkGhiMKbFjvYh1wNp4/B6amKJJ6BwAAAKAvJ6YULyem
        FAAAAAtzc2gtZWQyNTUxOQAAACAjyTJVHi3HRj31IDkGhiMKbFjvYh1wNp4/B6amKJJ6Bw
        AAAED/sa1axOMwTs3RxE9tKpppSP/aMVSVeGihFjVuB/qGHiPJMlUeLcdGPfUgOQaGIwps
        WO9iHXA2nj8HpqYoknoHAAAAFml0YWRtaW5AVk0tMS0xNy1jZW50b3MBAgMEBQYH
        -----END OPENSSH PRIVATE KEY-----"""

        _app_id_ = "86816166-240D-46D8-9BDD-CDE315D84DF0"
        _app_secret_ = "2E32AE814FFFA39B9915FED26E44B430"


        _ed25519_key_public_ = b"""ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICPJMlUeLcdGPfUgOQaGIwpsWO9iHXA2nj8HpqYoknoH itadmin@VM-1-17-centos"""

        # key = ECC.generate(curve='Ed25519')

        # with open('tplus','rt') as f:
        #     pv_key = ECC.import_key(f.read())
        pv_key = ECC.import_key(_ed25519_key_private_)

        # with open('tplus.pub','rt') as f:
            # pb_key = ECC.import_key(f.read())
        pb_key = ECC.import_key(_ed25519_key_public_)


        message = b'I give my permission to order #4355'
        prehashed_message = SHA512.new(message)
        signer = eddsa.new(pv_key, 'rfc8032')
        signature = signer.sign(prehashed_message)

        verifier = eddsa.new(pb_key, 'rfc8032')
        try:
            verifier.verify(prehashed_message, signature)
            print("The message is authentic")
        except ValueError:
            print("The message is not authentic")


    @staticmethod
    def success():
        return json.dumps(AppTicketActuator.__SUCCESS__)

    @staticmethod
    def failure():
        return json.dumps(AppTicketActuator.__FAILURE__)

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
        infomation = self.decrypt_push_message(content)
        AppTicketActuator._timber.debug("decrypt ticket: {infomation}")

        return AppTicket(infomation)

    def decrypt_push_message(self, content) -> dict:

        decrypt_key = self.actor_profile.cipher_key.encode("utf8")
        cipher = AES.new(decrypt_key, AES.MODE_ECB)

        ciphertext = content[AppTicketActuator.__ENCRYPT_MSG__]
        cipherbytes = bytes(ciphertext, encoding='utf8')
        raw_text = unpad(cipher.decrypt(base64.decodebytes(cipherbytes)), 16)
        infomation = raw_text.decode("utf8")

        return json.loads(infomation)


class TplusHttpCall(HttpCall):

    # __ACTOR_PROFILE__ = actuatorsEnvironment() \
    #                     .get_actor_profile(
    #                         actuatorsEnvironment.make_identifier(__module__, "AppTicketActor"))

    __BASE_URL__    = AppTicketActuator.__ACTOR_PROFILE__.base_url
    __APP_KEY__     = AppTicketActuator.__ACTOR_PROFILE__.app_key
    __APP_SECRET__  = AppTicketActuator.__ACTOR_PROFILE__.app_secret
    __CERTIFICATE__ = AppTicketActuator.__ACTOR_PROFILE__.app_token_certifcate
    __TICKET_PATH__ = AppTicketActuator.__ACTOR_PROFILE__.app_ticket_api_path
    __TOKEN_PATH__  = AppTicketActuator.__ACTOR_PROFILE__.app_token_api_path

    @Post(__TICKET_PATH__, headers =
         {
            TplusOpenApiProfile.__APP_KEY__: __APP_KEY__,
            TplusOpenApiProfile.__APP_SECRET__: __APP_SECRET__,
         })
    def refresh_app_ticket(self, response: httpx.Response) -> str:
        AppTicketActuator._timber.debug("TplusHttpCall.refresh_app_ticket()")

        if response.status_code != httpx.codes.OK:
            raise AppTicketRequestReject("Server rejected the request, check AppKey\AppSecrect. Doese target company match request?")
        
        return AppTicketActuator.success()
        

    @Post(__TOKEN_PATH__, headers =
         {
            TplusOpenApiProfile.__APP_KEY__: __APP_KEY__,
            TplusOpenApiProfile.__APP_SECRET__: __APP_SECRET__,
            "Content-Type": "application/json"
         })
    def exchange_app_token(self, response: httpx.Response):
        AppTicketActuator._timber.debug("TplusHttpCall.exchange_app_token()")
        
        if response.status_code != httpx.codes.OK:
            raise AppTicketRejectedByServer("App ticket rejected by server. Checked Certificates?")
        
        AppTicketActuator._timber.debug("get exchanged token: {response.text}")
        app_token = AppToken(response.json())

        return app_token.values_pack.token
