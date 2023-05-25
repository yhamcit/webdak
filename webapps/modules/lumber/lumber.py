
import logging

from logging import Logger
from logging.config import dictConfig

from webapps.language.decorators.singleton import Singleton

from webapps.model.properties.dao.lumber_environment import LumberEnvironment


@Singleton
class Lumber(object):

    def __init__(self, lumber_env) -> None:
        self._lumber_profile = LumberEnvironment(lumber_env)

    def build(self) -> None:
        dictConfig(self._lumber_profile.valueset)

    @staticmethod
    def timber(name: str) -> Logger:
        return logging.getLogger(name)
    
