from time import time
from datetime import datetime

import json
from typing import Union
from webapps.modules.lumber.lumber import Lumber
from webapps.plugins.cbs.errors.cbs_error import AppTokenInvalid

from webapps.plugins.cbs.model.dao.token_value_pack import AppTokenDataPack


class AppToken(object):

    _TEN_SECONDS_   = 10
    _HALF_MINUTE_   = 30
    _TEN_MINUTES_   = 10 * 60

    _CODE_          = "code"
    _MESSAGE_       = "msg"
    _DATA_          = "data"

    _SUCCESS_       = "0"

    _timber = Lumber.timber("model")

    def __init__(self, value: Union[str, dict]) -> None:

        if isinstance(value, str):
            valueset = json.loads(value)
        elif isinstance(value, dict):
            valueset = value
        else:
            raise AppTokenInvalid("", f"App Ticket must be one of (str, dict/json), got {type(value)} -{str(value)}")

        if valueset[AppToken._CODE_] == AppToken._SUCCESS_:
            self._data_pack = AppTokenDataPack(valueset[AppToken._DATA_])
            self._created_time = round(time())
        else:
            self._data_pack = None
            self._created_time = -1

        self._valueset = valueset


    def __str__(self) -> str:
        return json.dumps(self._valueset)

    @property
    def token(self) -> str:
        return self._data_pack.token

    @property
    def valueset(self) -> dict:
        return self._valueset

    @property
    def data_pack(self) -> AppTokenDataPack:
        return self._data_pack

    @property
    def code(self) -> dict:
        return self._valueset[AppToken._CODE_]

    @property
    def created_time(self) -> dict:
        return self._created_time

    @property
    def token_lifetime(self) -> int:
        cur_time = round(time())
        life_time = (self._data_pack.life_time + self._created_time) - cur_time
        AppToken._timber.warning(f"Token {json.dumps(self._valueset)} Create @{self._created_time} Now: {round(time())} life-time: {life_time}")
        return life_time

    def is_valid(self) -> bool:
        if self.created_time <= 0 or not self._data_pack:
            return False

        return self.token_lifetime >= AppToken._TEN_SECONDS_

