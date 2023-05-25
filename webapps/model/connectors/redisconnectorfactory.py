from redis import Redis
from redis.sentinel import Sentinel

from webapps.language.decorators.singleton import singleton
from webapps.language.errors.enverror import UnsupportedRedisMode

from webapps.model.properties.dao.redisenvironment import RedisEnvironment

@singleton
class RedisConnectorFactory(object):

    __STANDALONE__ = "standalone"
    __SENTINEL__ = "sentinel"
    __CLUSTER__ = "cluster"
    
    def __init__(self) -> None:
        pass

    def create_connector(self, redis_env: RedisEnvironment) -> Redis:

        if redis_env.mode == RedisConnectorFactory.__SENTINEL__:
            return self.create_sentinel_connection(redis_env)
        else:
            raise UnsupportedRedisMode("Database type: {} sepcified in environment configuration is not supported.".format(db_type))

    def create_sentinel_connection(self, redis_env: RedisEnvironment) -> Redis:

        sentinel = Sentinel(redis_env.sentinels, redis_env.connection_conf)
        return sentinel.master_for(redis_env.master_name)