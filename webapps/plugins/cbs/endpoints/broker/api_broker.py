
import json
import traceback
import base64

from datetime import datetime
from typing import Any
from httpx import ConnectTimeout, ReadTimeout, Response

from quart import ResponseReturnValue, request as view_request
from quart.views import View


from webapps.model.auth.access.access_errors import SerializableObjectNotAvialable
from webapps.model.auth.access.tic_tok_depot import SerializableObjectDepot
from webapps.modules.requests.httpcall import HttpCall
from webapps.modules.requests.httpcallbuilder import HttpCallBuilder
from webapps.modules.requests.httpheaderpod import HttpHeaderPod

from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.modules.requests.httpsession import HttpSession

from webapps.plugins.cbs.actuator.api_broker_call import CBSOpenapiBrokerHttpCall
from webapps.plugins.cbs.errors.cbs_error import AppTokenExpired, AppTokenInvalid
from webapps.plugins.cbs.model.auth.app_token import AppToken
from webapps.plugins.cbs.model.dao.api_broker_request import CBSRestfulapiBrokerRequest

from webapps.plugins.cbs.model.properties.cbs_endpoint_profile import CBSEndpointProfile
from webapps.plugins.cbs.model.properties.cbs_openapi_properties import CBSOpenApiProperties


from webapps.modules.lumber.lumber import Lumber

from asn1crypto.core import Sequence, Integer, IntegerOctetString

from webapps.modules.pygcrypt.pygcrypt import GM_T_0003_2_SM2 as sm2


class SM2Signature(Sequence):
    _fields = [
        ('r', Integer),
        ('s', Integer)
    ]

class SM2Cryptograhp(Sequence):
    _fields = [
        ('c1', IntegerOctetString),
        ('c2', IntegerOctetString),
        ('c3', IntegerOctetString)
    ]




class CBSRestfulapiBroker(PluginEndpoint):

    _timber = Lumber.timber("cbs")
    _err_timber = Lumber.timber("error")

    __ARGKEY_APP_ID__       = "app_id"
    __ARGKEY_APP_SECRET__   = "app_secret"

    _B64_STR_ENCODING_      = "utf-8"
    _CMB_CBS_ENCODING_      = "utf-8"

    class BrokerView(View):

        methods = ["GET", "POST"]

        def __init__(self, endpoint: PluginEndpoint) -> None:
            super().__init__()
            self._endpoint = endpoint

        async def dispatch_request(self, **kwargs: Any) -> ResponseReturnValue:

            if not CBSRestfulapiBrokerRequest._REQUEST_HEADER_CONTENT_TYPE_ in view_request.headers:
                return "A valid request must contain specified: 'Content-Type' as 'application/json'."

            content_type = view_request.headers.get(CBSRestfulapiBrokerRequest._REQUEST_HEADER_CONTENT_TYPE_)
            if (content_type != HttpHeaderPod._HDV_MIME_JSON_):
                return 'Content-Type not supported!'

            try:
                request = CBSRestfulapiBrokerRequest(await view_request.get_json())
                return await self._endpoint.request(request.api_path, request.api_method, request.body)      
            except ReadTimeout as excp_err:
                return f"Remote host network timeout: {excp_err.request}", 408
            except ConnectTimeout as excp_err:
                return f"Remote host connection timeout: {excp_err.request}", 408
            except Exception as error:
                CBSRestfulapiBroker._err_timber.error(f"{error}", f"{error.args}")

                return f"Request data can not be processed, reason: {error} - {str(error.args)}", 406


    def __init__(self, name: str, profile: CBSEndpointProfile, props: CBSOpenApiProperties) -> None:
        super().__init__(name, profile)

        self._profile = profile
        self._props = props
        self._conf_vault = dict()

        def decrypt_parser(http_call: HttpCall, response: Response, headers: HttpHeaderPod, session: HttpSession, **kwargs):

            headers = HttpHeaderPod(defaults=response.headers)

            if headers.test(CBSOpenapiBrokerHttpCall._X_MBCLOUD_ENCRYPTION_EN_, CBSOpenapiBrokerHttpCall._X_MBCLOUD_ENCRYPTION_TRUE_):
                http_call.response = self.decrypt_content(response.content)
            else:
                http_call.response = response.content
            
            return http_call

        
        self._seri_obj_depot = SerializableObjectDepot()
        self._http_call_builder = HttpCallBuilder(props.base_url)

        self._cipherware = sm2(pub_key=props.public_cipher_key, prv_key=props.private_cipher_key)

        self._http_parser = decrypt_parser

    def get_token(self) -> AppToken:
        try:
            app_token = AppToken(self._seri_obj_depot.get(self.__class__.__name__))

            if not app_token.is_valid():
                raise AppTokenExpired("App_Token expired", 
                                      f"token life time: {app_token.token_lifetime}", 
                                      (f"{app_token.created_time}", f"{app_token.data_pack.life_time}"))

            return app_token
        except KeyError as error:
            raise AppTokenInvalid(f"Token not exist", f"KeyError ID: {sself.__class__.__name__}", error.args)


    def put_token(self, app_token) -> str:
        return self._seri_obj_depot.put(app_token, self.__class__.__name__)


    def signature(self, bin_content: bytes, asn1 :bool=False) -> str:

        r, s = self._cipherware.sing_hash_sm3(data =bin_content)

        if asn1:
            signature = SM2Signature()
            signature['r'] = int.from_bytes(r)
            signature['s'] = int.from_bytes(s)

            sm2_sig = signature.dump(force = True)

        else:
            sm2_sig = r + s

        # print(" ============================= Asn.1 SIGNATURE Verify ==============================")

        # print(f"{sm2_sig.hex().upper()}")

        # if self._cipherware.verify(
        #     signature = bytes.fromhex('52BB67D2C6599E5C28EF0E96AFDB7CE54EDE0498CCAE55A6939632FB9687FC7B27D57632D1D485D72366EB35FC2099477000D4E93A4D91B4AE119420A544F86E'),
        #     _M='\n{"accountNo":""}&timestamp=1700279508863'.encode('utf-8')):

        #     print ("Java-bouncycastle :: Signature Match!")

        # raw_sig = r + s

        # if self._cipherware.verify(
        #     signature = raw_sig,
        #     _M=bin_content):

        #     print ("Python-libgcrypt :: Signature Match!")
        # print(" ============================= Asn.1 SIGNATURE Finish =============================")

        return base64.b64encode(sm2_sig).decode(CBSRestfulapiBroker._B64_STR_ENCODING_)


    def encrypt_content(self, bin_content: bytes, asn1 :bool=False) -> bytes:
        c1, c2, c3 = self._cipherware.encrypt(data =bin_content)

        if asn1:
            cipher = SM2Cryptograhp()
            cipher['c1'] = int.from_bytes(c1)
            cipher['c2'] = int.from_bytes(c2)
            cipher['c3'] = int.from_bytes(c3)

            sm2_cipher = cipher.dump(force = True)

        else:
            sm2_cipher = c1 + c2 + c3

        return sm2_cipher


    def decrypt_content(self, bin_content: bytes, asn1 :bool=False) -> bytes:

        if asn1:
            cipher = SM2Cryptograhp()
            cipher['c1'] = int.from_bytes(c1)
            cipher['c2'] = int.from_bytes(c2)
            cipher['c3'] = int.from_bytes(c3)

        else:
            c1 = bin_content[:65]
            c2 = bin_content[65:97]
            c3 = bin_content[97:]

        plain_binary = self._cipherware.decrypt(c1 =c1, c2 =c2, c3 =c3)

        return plain_binary


    async def requrie_token(self):

        json_params = {
            CBSRestfulapiBroker.__ARGKEY_APP_ID__: self._props.app_id, 
            CBSRestfulapiBroker.__ARGKEY_APP_SECRET__: self._props.app_secret,
            CBSOpenapiBrokerHttpCall._ARGKEY_GRANT_TYPE_: CBSOpenapiBrokerHttpCall._ARGVAL_CLIENT_CREDENTIALS_
        }

        http_call = self._http_call_builder.build(CBSOpenapiBrokerHttpCall)
        tok_text = await http_call.require_token(json =json_params)

        assert tok_text

        app_token = AppToken(tok_text)
        self.put_token(app_token)

        return app_token


    async def refresh_token(self, app_token: AppToken):

        headers = HttpHeaderPod(defaults={CBSOpenapiBrokerHttpCall._HDR_AUTHORIZATION_: f"Bearer {app_token.token}"})

        http_call = self._http_call_builder.build(CBSOpenapiBrokerHttpCall)
        http_call.update_http_headers(headers)

        tok_text = await http_call.refresh_token()

        return AppToken(tok_text)


    async def request(self, api_path: str, api_method: str, json_body: dict):

        app_token = None
        
        try:
            app_token = self.get_token()
        except (SerializableObjectNotAvialable, AppTokenExpired, AppTokenInvalid) as error:
            CBSRestfulapiBroker._timber.warning(f"Require another token needed: {error}")

            app_token = await self.requrie_token()
        except Exception as error:
            CBSRestfulapiBroker._err_timber(f"{error.args} \n {traceback.format_exc()}")
            raise error
        # else:
        #     app_token = await self.refresh_token(app_token)

        return await self.do_request(api_path, api_method, app_token, json_body)


    async def do_request(self, api_path: str, api_method: str, app_token: AppToken, json_body: dict):

        request_data = "\n" + json.dumps(json_body)
        request_data_bytes = bytes(request_data, encoding =CBSRestfulapiBroker._CMB_CBS_ENCODING_)
        
        timestamp = str(round(datetime.now().timestamp() * 1000))
        verifying_timestamp_bytes = CBSRestfulapiBroker.get_timestamp_bytes(timestamp)

        signature = self.signature(request_data_bytes + verifying_timestamp_bytes, asn1=True)

        cipher_bytes = self.encrypt_content(request_data_bytes)

        http_call = self._http_call_builder.build(CBSOpenapiBrokerHttpCall, api_path =api_path, api_method =api_method).set_response_parser(self._http_parser)

        headers = {
            CBSOpenapiBrokerHttpCall._HDR_AUTHORIZATION_: f"Bearer {app_token.token}", 
            CBSOpenapiBrokerHttpCall._HDR_X_MBCLOUD_API_SIGN_: signature,
            CBSOpenapiBrokerHttpCall._HDR_X_MBCLOUD_TIMESTAMP_: str(timestamp),
        }
        http_call.update_http_headers(HttpHeaderPod(defaults=headers))

        response = await http_call.broker_api_call(content =cipher_bytes)

        return response


    @staticmethod
    def get_timestamp_bytes(timestamp: str) -> bytes:
        return bytes(f"&timestamp={timestamp}", encoding = CBSRestfulapiBroker._CMB_CBS_ENCODING_)


    @property
    def view(self):
        return CBSRestfulapiBroker.BrokerView.as_view(self._profile.name, self)
    

