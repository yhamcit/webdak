from redis import Redis
from redis.sentinel import Sentinel

from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.env_errors import UnsupportedRedisMode

from webapps.model.properties.dao.redis_environment import RedisEnvironment

@Singleton
class RedisConnectorFactory(object):

    _STANDALONE_ = "standalone"
    _SENTINEL_ = "sentinel"
    _CLUSTER_ = "cluster"
    
    def __init__(self) -> None:
        pass

    def create_connector(self, redis_env: RedisEnvironment) -> Redis:

        if redis_env.mode == RedisConnectorFactory._SENTINEL_:
            return self.create_sentinel_connection(redis_env)
        else:
            raise UnsupportedRedisMode(f"Database type: {redis_env['db_type']} sepcified in environment configuration is not supported.")

    def create_sentinel_connection(self, redis_env: RedisEnvironment) -> Redis:

        sentinel = Sentinel(redis_env.sentinels, redis_env.connection_conf)
        return sentinel.master_for(redis_env.master_name)