
from webapps.language.decorators.singleton import singleton


@singleton
class LumberEnvironment(object):

    __TAG__ = "tag"
    __LOG_PATH__ = "log_path"
    __FORMATTERS__ = "formatters"
    __HANDLERS__ = "handlers"
    __LOGGERS__ = "loggers"

    def __init__(self) -> None:
        self._environment = None

    @property
    def environment(self) -> str:
        return self._environment

    @environment.setter
    def environment(self, profile):
        self._environment = profile

    @property
    def formatters(self) -> str:
        return self.environment[LumberEnvironment.__LOG_PATH__]

    @property
    def formatters(self) -> dict:
        return self.environment[LumberEnvironment.__FORMATTERS__]
    
    @property
    def handlers(self) -> dict:
        return self.environment[LumberEnvironment.__HANDLERS__]
    
    @property
    def handlers(self) -> dict:
        return self.environment[LumberEnvironment.__LOGGERS__]
