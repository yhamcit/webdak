from typing import Any

from base64 import b64encode
from os import urandom
from random import randint, sample
from hashlib import sha1, shake_256
from time import time as  timestamp
from json import dumps

import httpx
from quart.views import View

from quart import request as view_request

from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.plugins.publicdebt.model.dao.wecorp_acctoken import CorpWechatAccToken
from webapps.plugins.publicdebt.model.dao.wecorp_jsapiticket import CorpWechatJSApiTicket
from webapps.plugins.publicdebt.model.properties.debtquery import DebtQueryProfile, DebtQueryProperties



class CorpWeChatAuthorition(PluginEndpoint):

    _timber = Lumber.timber("wechat_authorition")
    _err_timber = Lumber.timber("error")

    _REQUEST_HEADER_CONTENT_TYPE_ = "Content-Type"
    __REQUEST_PARAM_URL__ = 'url'

    class AuthView(View):

        methods = ["GET", "POST"]

        def __init__(self, endpoint: PluginEndpoint) -> None:
            super().__init__()
            self._endpoint = endpoint

        async def dispatch_request(self, **kwargs: Any) -> dict:

            content_type = view_request.headers.get(CorpWeChatAuthorition._REQUEST_HEADER_CONTENT_TYPE_)
            if (content_type != HttpHeaderPod._HDV_MIME_JSON_):
                return 'Content-Type not supported!'

            try:
                request = await view_request.get_json()

                return await self._endpoint.request(request[CorpWeChatAuthorition.__REQUEST_PARAM_URL__])
            except Exception as error:
                return f"Request data can not be processed, reason: {error} - {str(error.args)}", 406


    @property
    def view(self):
        return CorpWeChatAuthorition.AuthView.as_view(self._profile.name, self)



    def __init__(self, name: str, profile: DebtQueryProfile, props: DebtQueryProperties) -> None:
        super().__init__(name, profile)

        self._profile = profile
        self._props = props
        self._conf_vault = dict()
        self._acc_token = None
        self._jsapi_ticket = None


    async def get_access_token(self):

        if self._acc_token == None or self._acc_token.is_expired():

            self._acc_token = None

            corpid = 'wwd2c8180973870229'
            agentid = '1000017'   # 资产平台 Agent ID，其它应用认证时需要替换
            appsecret = 's0l5xxaXSRAOccOZ0wsaF_AkrXvTuRQvREBhfkuTBX8'   # 资产平台 secret，其它应用认证时需要替换

            params = {'corpid': corpid, 'corpsecret': appsecret}
            async with httpx.AsyncClient() as client:
                response = await client.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', params=params)

            # {
            #    "errcode": 0,
            #    "errmsg": "ok",
            #    "access_token": "accesstoken000001",
            #    "expires_in": 7200
            # }
            acctok = CorpWechatAccToken(from_json=response.json())

            if acctok.errcode != 0:
                raise
            else:
                self._acc_token = acctok

        return self._acc_token.access_token
        

    async def get_jsapi_ticket(self):

        if self._jsapi_ticket == None or self._jsapi_ticket.is_expired():

            self._jsapi_ticket = None

            acc_tok = await self.get_access_token()

            params = {'access_token': acc_tok}
            async with httpx.AsyncClient() as client:
                response = await client.get('https://qyapi.weixin.qq.com/cgi-bin/get_jsapi_ticket', params=params)

            # {
            #     "errcode":0,
            #     "errmsg":"ok",
            #     "ticket":"bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA",
            #     "expires_in":7200
            # }
            jsapi_tic = CorpWechatJSApiTicket(from_json=response.json())

            if jsapi_tic.errcode != 0:
                raise Exception()
            else:
                self._jsapi_ticket = jsapi_tic

        return self._jsapi_ticket.ticket


    @staticmethod
    def generate_nonce(length=16):
        """Generate pseudorandom number."""
        # return ''.join([str(randint(0, 9)) for i in range(length)])
        # return str(randint(0, 100000000))


        bincs = b64encode(urandom(length * 2), altchars=b'-_')
        nonce_lst = sample(tuple(bincs.decode('utf-8')), length)

        return ''.join(nonce_lst)



    async def request(self, sig_url: str):
        json = dict()

        json['jsapi_tic'] = await self.get_jsapi_ticket()
        json['nonce'] = CorpWeChatAuthorition.generate_nonce(16)
        json['timestamp'] = str(int(timestamp()))
        json['url'] = sig_url

        str_to_sign = '&'.join('='.join((k, v)) for k, v in json.items())
        sha1_alg = sha1()
        sha1_alg.update(str_to_sign.encode('utf-8'))
        json['signature'] = sha1_alg.hexdigest()

        json['nonceStr'] = json.pop('nonce')

        return dumps(json)

 
