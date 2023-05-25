
from webapps.language.decorators.singleton import Singleton

@Singleton
class RedisEnvironment(object):

    _MODE_ = "mode"
    _SENTINEL_ = "sentinels"
    _MASTER_ = "master_name"
    _CONNECTION_CONF_ = "connection_conf"

    def __init__(self, valueset: dict) -> None:
        self._valueset = valueset

    @property
    def valueset(self) -> tuple:
        return self._valueset

    @valueset.setter
    def valueset(self, valueset: dict) -> tuple:
        self._valueset = valueset

    @property
    def sentinels(self) -> tuple:
        return tuple(tuple(d.values()) for d in self.sentinel_profiles)
    
    @property
    def mode(self) -> setattr:
        return self.valueset[RedisEnvironment._MODE_]
    
    @property
    def master_name(self) -> setattr:
        return self.valueset[RedisEnvironment._MASTER_]
    
    @property
    def connection_conf(self) -> dict:
        return self.valueset[RedisEnvironment._CONNECTION_CONF_]
    
    @property
    def sentinel_profiles(self) -> tuple:
        return self.valueset[RedisEnvironment._SENTINEL_]