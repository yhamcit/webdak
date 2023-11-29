



from webapps.plugins.cbs.errors.cbs_error import AppTokenInvalid


class AppTokenDataPack(object):

    _TOKEN_         = "token"
    _TOKEN_TYPE_    = "token_type"
    _TOKENTYPE_     = "tokenType"
    _EXPIRES_       = "expires"

    def __init__(self, valueset: dict) -> None:
        try:
            self._token = valueset[AppTokenDataPack._TOKEN_]
            if AppTokenDataPack._TOKEN_TYPE_ in valueset:
                self._token_type = valueset[AppTokenDataPack._TOKEN_TYPE_]
            elif AppTokenDataPack._TOKENTYPE_ in valueset:
                self._token_type = valueset[AppTokenDataPack._TOKENTYPE_]

            self._expires = int(valueset[AppTokenDataPack._EXPIRES_])
        except KeyError as error:
            raise AppTokenInvalid(error)
        except Exception as error:
            raise error
    @property
    def token(self) -> str:
        return self._token

    @property
    def type(self) -> str:
        return self._token_type

    @property
    def life_time(self) -> int:
        return self._expires
