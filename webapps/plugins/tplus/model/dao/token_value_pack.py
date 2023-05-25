

from webapps.plugins.tplus.model.dao.tplus_errors import TplusPushMsgException


class AppTokenValuePack(object):

    __ACCESS_TOKEN__            = "accessToken"
    __REFRESH_TOKEN__           = "refreshToken"
    __SCOPE__                   = "scope"
    __EXPIRES_IN__              = "expiresIn"
    __USER_ID__                 = "userId"
    __ORGNIZATION_ID__          = "orgId"
    __APP_NAME__                = "appName"
    __REFRESH_TOKEN_EXPIRE_IN__ = "refreshExpiresIn"

    def __init__(self, valueset: dict) -> None:
        try:
            self._access_token = valueset[AppTokenValuePack.__ACCESS_TOKEN__]
            self._refresh_token = valueset[AppTokenValuePack.__REFRESH_TOKEN__]
            self._scope = valueset[AppTokenValuePack.__SCOPE__]
            self._access_token_lifetime = int(valueset[AppTokenValuePack.__EXPIRES_IN__])
            self._user_id = valueset[AppTokenValuePack.__USER_ID__]
            self._org_id = valueset[AppTokenValuePack.__ORGNIZATION_ID__]
            self._app_name = valueset[AppTokenValuePack.__APP_NAME__]
            self._refresh_token_lifetime = int(valueset[AppTokenValuePack.__REFRESH_TOKEN_EXPIRE_IN__])
        except KeyError as error:
            raise TplusPushMsgException(f"{error}")

    @property
    def access_token(self) -> str:
        return self._access_token
    
    @property
    def refresh_token(self) -> str:
        return self._refresh_token
    
    @property
    def access_expiration(self) -> int:
        return self._access_token_lifetime
    
    @property
    def refresh_expiration(self) -> int:
        return self._refresh_token_lifetime
    
    @property
    def app_name(self) -> str:
        return self._app_name
    

