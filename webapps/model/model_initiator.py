

from webapps.language.decorators.singleton import Singleton

from webapps.modules.lumber.lumber import Lumber

from webapps.model.properties.environments import Evironments


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

    def ready(self):
        Lumber(self._app_env.logging).build()

        return self
