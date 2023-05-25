
from webapps.language.decorators.singleton import singleton

@singleton
class RedisEnvironment(object):

    __MODE__ = "mode"
    __SENTINEL__ = "sentinels"
    __MASTER__ = "master_name"
    __CONNECTION_CONF__ = "connection_conf"

    def __init__(self) -> None:
        self._environment = None

    @property
    def environment(self) -> tuple:
        return self._environment

    @environment.setter
    def environment(self, redis_env: dict) -> tuple:
        self._environment = redis_env

    @property
    def sentinels(self) -> tuple:
        return tuple(tuple(d.values()) for d in self.sentinel_profiles)
    
    @property
    def mode(self) -> setattr:
        return self.environment[RedisEnvironment.__MODE__]
    
    @property
    def master_name(self) -> setattr:
        return self.environment[RedisEnvironment.__MASTER__]
    
    @property
    def connection_conf(self) -> dict:
        return self.environment[RedisEnvironment.__CONNECTION_CONF__]
    
    @property
    def sentinel_profiles(self) -> tuple:
        return self.environment[RedisEnvironment.__SENTINEL__]