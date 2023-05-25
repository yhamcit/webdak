
from webapps.language.decorators.singleton import singleton


@singleton
class PromisePoolEnvironment(object):

    __CHANNELS__ = "channels"
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
        return self._environment[PromisePoolEnvironment.__CHANNELS__]