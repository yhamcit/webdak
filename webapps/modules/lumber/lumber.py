
import logging
from logging import Logger
from logging.config import dictConfig

from webapps.language.decorators.singleton import singleton

from webapps.model.properties.dao.lumberenvironment import LumberEnvironment


@singleton
class Lumber(object):

    def __init__(self, lumber_env) -> None:
        self._lumber_profile = LumberEnvironment()
        self._lumber_profile.profile = lumber_env

    def build(self) -> None:
        dictConfig(self._lumber_profile.profile)

    @staticmethod
    def timber(name: str) -> Logger:
        return logging.getLogger(name)
    
