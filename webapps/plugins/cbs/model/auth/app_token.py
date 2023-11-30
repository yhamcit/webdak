from time import time

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
            self._code = valueset[AppToken._CODE_]


    def __str__(self) -> str:
        return json.dumps(self._data_pack)

    @property
    def token(self) -> str:
        return self._data_pack.token

    @property
    def valueset(self) -> dict:
        return self._data_pack

    @property
    def data_pack(self) -> AppTokenDataPack:
        return self._data_pack

    @property
    def code(self) -> str:
        return self._code

    @property
    def token_lifetime(self) -> int:
        return self._data_pack.life_time

    def is_valid(self) -> bool:
        if not hasattr(self, '_data_pack'):
            return False

        AppToken._timber.warning(f"Token {self._data_pack.token} life-time: {self.token_lifetime} now: {round(time())}, life-left: {self.token_lifetime - round(time())}")

        return self.token_lifetime - round(time()) >= AppToken._TEN_SECONDS_

