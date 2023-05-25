
from sqlalchemy import create_engine

from webapps.language.decorators.singleton import singleton
from webapps.model.properties.environments import Evironments
from webapps.model.connectors.dbconnectorfactory import DatabaseConnectorFactory
from webapps.model.connectors.redisconnectorfactory import RedisConnectorFactory
from webapps.model.properties.dao.databaseenvironment import DatabaseEnvironment
from webapps.model.properties.dao.redisenvironment import RedisEnvironment
from webapps.model.properties.dao.actorenvironment import ActorsEnvironment
from webapps.model.properties.dao.lumberenvironment import LumberEnvironment
from webapps.modules.lumber.lumber import Lumber

@singleton
class ModelInitiator(object):
    
    def __init__(self) -> None:
        self._app_env = Evironments()
        self._lumber_env_vault = LumberEnvironment()
        self._lumber_env_vault.environment = self._app_env.logging
        self._db_env_vault = DatabaseEnvironment()
        self._db_env_vault.environment = self._app_env.database
        self._redis_env_vault = RedisEnvironment()
        self._redis_env_vault.environment = self._app_env.redis
        self._actors_env_vault = ActorsEnvironment()
        self._actors_env_vault.environment = self._app_env.actors
        self._databases = dict()
        self._redis = None

    def boot(self):
        Lumber(self._app_env.logging).build()

        return self

    def init_database_connection(self):
        for id, env in self.db_env_vault:
            self._databases[id] = DatabaseConnectorFactory()\
                .create_connector(env)

        return self

    def init_redis_connection(self):
        self._redis = RedisConnectorFactory() \
            .create_connector(self.redis_env_vault)

        return self
    
    @property
    def lumber_env_vault(self) -> DatabaseEnvironment:
        return self._lumber_env_vault
    
    @property
    def db_env_vault(self) -> DatabaseEnvironment:
        return self._db_env_vault
    
    @property
    def redis_env_vault(self) -> RedisEnvironment:
        return self._redis_env_vault
