

from webapps.language.decorators.singleton import Singleton

from webapps.modules.lumber.lumber import Lumber

from webapps.model.properties.environments import Evironments

from webapps.model.connectors.db_connector_factory import DatabaseConnectorFactory
from webapps.model.connectors.redisconnectorfactory import RedisConnectorFactory

from webapps.model.properties.dao.plugin_environment import PluginEnvironment
from webapps.model.properties.dao.database_environment import DatabaseEnvironment
from webapps.model.properties.dao.redis_environment import RedisEnvironment
from webapps.model.properties.dao.lumber_environment import LumberEnvironment

@Singleton
class ModelInitiator(object):
    
    def __init__(self) -> None:
        self._app_env = Evironments()
        self._app_env.load()

        self._lumber_env_vault = LumberEnvironment(self._app_env.logging)
        self._db_env_vault = DatabaseEnvironment(self._app_env.database)
        self._redis_env_vault = RedisEnvironment(self._app_env.redis)
        self._plugin_env_vault = PluginEnvironment(self._app_env.plugins)
        self._databases = dict()
        self._redis = None

    def boot(self):
        Lumber(self._app_env.logging).build()

        return self

    def init_database_connection(self):
        for profile in self.db_env_vault:
            self._databases[profile.identifier] = DatabaseConnectorFactory().create_connector(profile)

        return self

    def init_redis_connection(self):
        self._redis = RedisConnectorFactory().create_connector(self.redis_env_vault)

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
