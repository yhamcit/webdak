
from webapps.language.decorators.singleton import Singleton


@Singleton
class LumberEnvironment(object):

    _TAG_ = "tag"
    _LOG_PATH_ = "log_path"
    _FORMATTERS_ = "formatters"
    _HANDLERS_ = "handlers"
    _LOGGERS_ = "loggers"

    def __init__(self, valueset: dict) -> None:
        self._valueset = valueset

    @property
    def valueset(self) -> dict:
        return self._valueset

    @valueset.setter
    def valueset(self, profile):
        self._valueset = profile

    @property
    def formatters(self) -> str:
        return self.valueset[LumberEnvironment._LOG_PATH_]

    @property
    def formatters(self) -> dict:
        return self.valueset[LumberEnvironment._FORMATTERS_]
    
    @property
    def handlers(self) -> dict:
        return self.valueset[LumberEnvironment._HANDLERS_]
    
    @property
    def handlers(self) -> dict:
        return self.valueset[LumberEnvironment._LOGGERS_]
