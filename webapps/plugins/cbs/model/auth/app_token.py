from time import time
from datetime import datetime

import json
from webapps.plugins.cbs.errors.cbs_error import AppTokenInvalid

from webapps.plugins.cbs.model.dao.token_value_pack import AppTokenDataPack


class AppToken(object):

    _TEN_SECONDS_   = 10 * 1000
    _HALF_MINUTE_   = 30 * 1000
    _TEN_MINUTES_   = 10 * 60 * 1000

    _CODE_          = "code"
    _MESSAGE_       = "msg"
    _DATA_          = "data"

    _SUCCESS_       = "0"

    def __init__(self, value: (dict, str)) -> None:

        if isinstance(value, str):
            valueset = json.loads(value)
        if isinstance(value, dict):
            valueset = value
        else:
            raise AppTokenInvalid(f"App Ticket must be one of (str, dict/json), got {type(value)} -{str(value)}")

        if valueset[AppToken._CODE_] == AppToken._SUCCESS_:
            self._data_pack = AppTokenDataPack(valueset[AppToken._DATA_])
            self._created_time = round(datetime.now().timestamp() * 1000)
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
        return (self._data_pack.life_time + self._created_time) - time() * 1000

    def is_valid(self) -> bool:
        if self.created_time <= 0 or not self._data_pack:
            return False

        return self.token_lifetime >= AppToken._TEN_SECONDS_

