
from time import time
from typing import Any


class AppTokenDataPack(dict):

    _TOKEN_         = "token"
    _TOKEN_TYPE_    = "token_type"
    _TOKENTYPE_     = "tokenType"
    _EXPIRES_       = "expires"
    _LIFE_TIME_     = "life_time"

    def __init__(self, *args, **kwargs) -> None:
        self.update(*args, **kwargs)
        self.life_time = int(self[AppTokenDataPack._EXPIRES_])

    def __repr__(self) -> str:
        return super().__repr__()

    @property
    def token(self) -> str:
        return self[AppTokenDataPack._TOKEN_]

    @property
    def type(self) -> str:
        if AppTokenDataPack._TOKEN_TYPE_ in self:
            return self.self[AppTokenDataPack._TOKEN_TYPE_]
        else:
            return self.self[AppTokenDataPack._TOKENTYPE_]

    @property
    def life_time(self) -> int:
        return self.self[AppTokenDataPack._LIFE_TIME_]
    
    @life_time.setter
    def life_time(self, expire_time: int):
        self[AppTokenDataPack._LIFE_TIME_] = expire_time + round(time())
