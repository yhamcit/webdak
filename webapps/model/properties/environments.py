from os import environ
import argparse

import rtoml

from pathlib import Path

from webapps.model.properties.dao.databaseenvironment import DatabaseEnvironment
from webapps.language.decorators.singleton import singleton

from webapps.language.errors.enverror import ConfigFileError
from webapps.language.errors.enverror import ConfigContentError

@singleton
class Evironments(object):

    __DEPLOYMENT__ = "deployment"
    __PROMISEPOOl__ = "promisepool"
    __LOGGING__ = "lumber"
    __REDIS__ = "redis"
    __DATABASE__ = "database"
    __ACTORS__ = "actors"

    def __init__(self) -> None:
        __CONFIG_ENV = "WEBDAK_CONF"
        __CONFIG_PATH = "./conf/webdak.conf.d/default.toml"

        parser = argparse.ArgumentParser(description='Starts web-dak service.')

        parser.add_argument("-c", "--config", 
                                help = "Specify the path to load configuration file.", type = str)
        
        args, unkown = parser.parse_known_args()

        conf_uri = __CONFIG_PATH
        if args.config:
            conf_uri = args.config
        elif __CONFIG_ENV in environ:
            conf_uri = environ[__CONFIG_ENV]

        try:
            self._configuration = rtoml.load(Path(conf_uri))
        except FileNotFoundError as error:
            # TODO: dig error context & info
            raise ConfigFileError()
        except Exception as error:
            # TODO: dig error context & info
            raise ConfigContentError()

    @property
    def deployment(self) -> dict:
        return self._configuration[Evironments.__DEPLOYMENT__]
    
    @property
    def promisepool(self) -> dict:
        return self._configuration[Evironments.__PROMISEPOOl__]
    
    @property
    def logging(self) -> dict:
        return self._configuration[Evironments.__LOGGING__]

    @property
    def deployment(self) -> list:
        return self._configuration[Evironments.__DEPLOYMENT__]

    @property
    def redis(self) -> list:
        return self._configuration[Evironments.__REDIS__]

    @property
    def database(self) -> dict:
        return self._configuration[Evironments.__DATABASE__]

    @property
    def actors(self) -> dict:
        return self._configuration[Evironments.__ACTORS__]
    
    # @database.setter
    # def database(self, db_type: str) -> None:
    #     # TODO: initialize db library/db connection property
    #     self.__db_type = db_type
    
    # @db_conn.setter
    # def db_conn(self, db_conn: DatabaseConnection) -> None:
    #     self.__db_conn = db_conn



