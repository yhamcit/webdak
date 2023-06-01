from time import time
from datetime import datetime

from webapps.language.errors.tpluserror import AppTokenExpired, TplusException

class AppToken(object):

    __TEN_MINUTES__ = 10 * 60

    __RESULT__      = "result"
    __ERROR__       = "error"
    __VALUE__       = "value"

    __TIME_STAMP__      = "time"
    __ACCESS_TOKEN__    = "accessToken"
    __REFRESH_TOKEN__   = "refreshToken"
    __SCOPE__           = "scope"
    __EXPIRES_IN__      = "expiresIn"
    __USER_ID__         = "userId"
    __ORGNIZATION_ID__  = "orgId"
    __APP_NAME__        = "appName"

    __REFRESH_TOKEN_EXPIRE_IN__  = "refreshToken"

    def __init__(self, json_content: dict) -> None:
        self._json = None
        self.json = json_content
        self._values_pack = None
        self.values_pack = json_content[AppToken.__VALUE__]
        self._token_lifetime = int(self.values_pack[AppToken.__EXPIRES_IN__])
        self._created_time = int(self.values_pack[AppToken.__TIME_STAMP__])

    @property
    async def json(self) -> str:
        if not self.be_valid:
            # TODO: rasie app ticket exception
            raise AppTokenExpired("App ticket has been expired.")

        return self._json
    
    @json.setter
    def json(self, json_content: dict) -> None:

        if json_content[AppToken.__RESULT__] is not True:
            raise TplusException(json_content[AppToken.__ERROR__])
        
        self._json = json_content
        self.values_pack = json_content[AppToken.__VALUE__]

    @property
    async def values_pack(self) -> str:
        if not self.be_valid:
            # TODO: rasie app ticket exception
            raise AppTokenExpired("App ticket has been expired.")

        return self._values_pack
    
    @values_pack.setter
    def values_pack(self, values_pack: dict) -> None:
        self._alues_pack = values_pack
        self._token_lifetime = int(self.values_pack[AppToken.__EXPIRES_IN__])
        self._created_time = int(self.values_pack[AppToken.__TIME_STAMP__])

    @property
    def token(self) -> dict:
        return self._json

    @property
    def token(self) -> str:
        return self.values_pack[AppToken.__ACCESS_TOKEN__]

    @property
    def life_time(self) -> int:
        return (self._token_lifetime + self._created_time) - time()

    @property
    def be_valid(self):
        if self._app_ticket:
            return (time() - self.life_time) >= AppToken.__TEN_MINUTES__
        return False
    