
from webapps.language.decorators.singleton import Singleton


@Singleton
class PromisePoolEnvironment(object):

    _CHANNELS_ = "channels"
    def __init__(self) -> None:
        self._environment = None

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, promise_env) -> None:
        self._environment = promise_env
    
    @property
    def channels(self) -> tuple:
        return self._environment[PromisePoolEnvironment._CHANNELS_]