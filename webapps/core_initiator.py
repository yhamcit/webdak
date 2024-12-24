

from webapps.model.properties.environments import Evironments
from webapps.model.properties.dao.promisepool_environment import PromisePoolEnvironment
from webapps.modules.coroutinpromise.promisepool import PromisePool


class SystemInitiator(object):

    def __init__(self) -> None:
        self._app_env = Evironments()
        # self._promisepool_env_vault = PromisePoolEnvironment()
        # self._promisepool_env_vault.environment = self._app_env.promisepool

    def boot(self) :
        return self
    
    def init_promise_pool(self):
        self._promise_pool = PromisePool()
        return self

