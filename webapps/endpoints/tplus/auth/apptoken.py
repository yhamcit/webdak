from time import time

from webapps.language.errors.tpluserror import AppTokenExpired, TplusException, AppTokenUninitialized

class AppTokenErrorDescription(object):
    __CODE__    = "code"
    __MSG__     = "msg"
    __HINT__    = "hint"

    def __init__(self, error_des: dict) -> None:
        self._raw = None

        self._code = ''
        self._msg = ''
        self._hint = ''

        if error_des:
            self.errors = error_des

    @property
    def code(self) -> str:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def hint(self) -> str:
        return self._hint

    @property
    def errors(self) -> dict:
        return self._raw

    @errors.setter
    def errors(self, error_des: dict) -> None:
        if AppTokenErrorDescription.__CODE__ in error_des:
            self._code = error_des[AppTokenErrorDescription.__CODE__]

        if AppTokenErrorDescription.__MSG__ in error_des:
            self._msg = error_des[AppTokenErrorDescription.__MSG__]

        if AppTokenErrorDescription.__HINT__ in error_des:
            self._hint = error_des[AppTokenErrorDescription.__HINT__]
    
class AppTokenValuePack(object):

    __ACCESS_TOKEN__    = "accessToken"
    __REFRESH_TOKEN__   = "refreshToken"
    __SCOPE__           = "scope"
    __EXPIRES_IN__      = "expiresIn"
    __USER_ID__         = "userId"
    __ORGNIZATION_ID__  = "orgId"
    __APP_NAME__        = "appName"
    __REFRESH_TOKEN_EXPIRE_IN__  = "refreshToken"

    def __init__(self, value_pack: dict) -> None:
        self._raw_values = None

        self._access_token = ''
        self._refresh_token = ''
        self._scope = ''
        self._expire_in = -1
        self._user_id = ''
        self._org_id = ''
        self._app_name = ''
        self._refresh_expire_in = -1
        
        if value_pack:
            self.values_pack = value_pack

    @property
    def values(self) -> str:
        if not self.be_valid:
            # TODO: rasie app ticket exception
            raise AppTokenExpired("App ticket has been expired.")

        return self._raw
    
    @values.setter
    def values(self, values: dict) -> None:
        try:
            self._access_token = values[AppTokenValuePack.__ACCESS_TOKEN__]
            self._refresh_token = values[AppTokenValuePack.__REFRESH_TOKEN__]
            self._scope = values[AppTokenValuePack.__SCOPE__]
            self._expire_in = int(values[AppTokenValuePack.__EXPIRES_IN__])
            self._user_id = values[AppTokenValuePack.__USER_ID__]
            self._org_id = values[AppTokenValuePack.__ORGNIZATION_ID__]
            self._app_name = values[AppTokenValuePack.__APP_NAME__]
            self._refresh_expire_in = int(values[AppTokenValuePack.__REFRESH_TOKEN_EXPIRE_IN__])

            self._raw_values = values
        except KeyError as err:
            # TODO: handle value error (debug)
            pass

    @property
    def token(self) -> str:
        return self._access_token

    @property
    def life_time(self) -> str:
        return self._expire_in

    @property
    def validation(self) -> bool:
        if self._expire_in <= 0 or self._refresh_expire_in <= 0:
            raise AppTokenUninitialized("App ticket has been expired.")

        return True

class AppToken(object):

    __HALF_MINUTE__  = 30
    
    __TEN_MINUTES__ = 10 * 60

    __RESULT__      = "result"
    __ERROR__       = "error"
    __VALUE__       = "value"

    def __init__(self, json_content: dict) -> None:
        self._json = json_content

        if AppToken.__ERROR__ in json_content:
            self._err_des = AppTokenErrorDescription(json_content[AppToken.__ERROR__])

        if AppToken.__VALUE__ in json_content:
            self._values_pack = AppTokenValuePack(json_content[AppToken.__VALUE__])
            self._created_time = time()
        else:
            self._created_time = -1

    @property
    def is_token_valid(self):
        if self.created_time <= 0:
            return False

        self.values_pack.validation()            
        return self.token_lifetime >= AppToken.__HALF_MINUTE__

    @property
    def created_time(self) -> dict:
        return self._created_time

    @property
    def values_pack(self) -> dict:
        return self._values_pack

    @property
    def token_lifetime(self) -> int:
        return (self.values_pack.life_time + self.created_time) - time()
    