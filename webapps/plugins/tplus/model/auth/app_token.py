from time import time
import json

from webapps.plugins.tplus.model.dao.token_error_des import AppTokenErrorDescription
from webapps.plugins.tplus.model.dao.token_value_pack import AppTokenValuePack
from webapps.plugins.tplus.model.dao.tplus_errors import AppTokenInvalid


class AppToken(object):

    _TEN_SECONDS_   = 10
    _HALF_MINUTE_   = 30
    _TEN_MINUTES_   = 10 * 60

    _RESULT_        = "result"
    _ERROR_         = "error"
    _VALUE_         = "value"

    _CREATE_TIME_   = "_CREATE_TIME_"

    def __init__(self, value: (dict, str)) -> None:

        if isinstance(value, str):
            valueset = json.loads(value)
        elif isinstance(value, dict):
            valueset = value
        else:
            raise AppTokenInvalid(f"Received token must be one of (str, dict/json), got {type(value)} -{str(value)}")
        self._valueset = valueset

        if not AppToken._CREATE_TIME_ in valueset:
            self._create_time = int(time())
            valueset[AppToken._CREATE_TIME_] = self._create_time
        else:
            self._create_time = valueset[AppToken._CREATE_TIME_]

        if AppToken._ERROR_ in valueset and valueset[AppToken._ERROR_]:
            self._err_des = AppTokenErrorDescription(valueset[AppToken._ERROR_])
            raise AppTokenInvalid(f"Received token contain {AppToken._ERROR_} which indicates a invalid response: {valueset[AppToken._ERROR_]}")
        elif AppToken._VALUE_ in valueset:
            self._value_pack = AppTokenValuePack(valueset[AppToken._VALUE_])
        elif AppToken._RESULT_ in valueset:
            self._value_pack = AppTokenValuePack(valueset[AppToken._RESULT_])
        else:
            raise AppTokenInvalid(f"App token must contain one of ({AppToken._VALUE_}, {AppToken._RESULT_}), got {type(value)} -{str(value)}")

    def __str__(self) -> str:
        return json.dumps(self._valueset)

    @property
    def valueset(self) -> dict:
        return self._valueset

    @valueset.setter
    def content_pack(self, valueset: dict):
        self.__init__(valueset)

    @property
    def access_token(self) -> str:
        return self._value_pack._access_token

    @property
    def refresh_token(self) -> str:
        return self._value_pack._refresh_token

    @property
    def is_token_valid(self):
        if self.created_time <= 0:
            return False

        return self.access_token_lifetime >= AppToken._HALF_MINUTE_

    @property
    def error(self) -> dict:
        return self._valueset[AppToken._ERROR_]

    @property
    def create_time(self) -> dict:
        return self._create_time

    @property
    def access_token_lifetime(self) -> int:
        return (self._value_pack.access_expiration + self._create_time) - int(time())

    @property
    def access_token(self) -> str:
        return self._value_pack.access_token

    @property
    def refresh_token_lifetime(self) -> int:
        return (self._value_pack.refresh_expiration + self._create_time) - int(time())
    
    @property
    def is_valid(self) -> bool:
        if not self._value_pack:
            return False

        return self.access_token_lifetime >= AppToken._TEN_SECONDS_

    @property
    def is_expired(self) -> bool:
        if not self._value_pack:
            return False
        
        return self.refresh_token_lifetime >= AppToken._TEN_SECONDS_
