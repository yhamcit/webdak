from os import environ, listdir
from os.path import join as joinpath, splitext, basename, isdir, isfile

import argparse
from pathlib import Path

from tomli import load

from webapps.modules.lumber.lumber import Lumber
from webapps.language.decorators.singleton import Singleton

from webapps.model.properties.dao.env_errors import ConfigFileError
from webapps.model.properties.dao.env_errors import ConfigContentError


_err_timber = Lumber.timber("error")


@Singleton
class Evironments(object):

    _DEPLOYMENT_        = "deployment"
    _PROMISEPOOl_       = "promisepool"
    _LOGGING_           = "lumber"
    _REDIS_             = "redis"
    _DATABASE_          = "database"
    _PLUGINS_           = "plugins"
    _PLUGIN_INCLUDES_   = "includes"

    _CONFIG_ENV_        = "WEBDAK_CONF"
    _CONFIG_PATH_       = "./conf/default.toml"


    def __init__(self) -> None:
        self._configuration = None

        parser = argparse.ArgumentParser(description='Starts webdak service.')
        parser.add_argument("-c", "--config", 
                                help = "Specify the path to load configuration file.", type = str)
        args, unkown = parser.parse_known_args()

        self.conf_uri = Evironments._CONFIG_PATH_
        if args.config:
            self.conf_uri = args.config
        elif Evironments._CONFIG_ENV_ in environ:
            self.conf_uri = environ[Evironments._CONFIG_ENV_]


    def load(self):
        with open(Path(self.conf_uri).absolute(), "rb") as f:
            try:
                self._configuration = load(f)
            except FileNotFoundError:
                # TODO: dig error context & info
                raise
            except Exception:
                # TODO: dig error context & info
                raise

    @property
    def promisepool(self) -> dict:
        return self._configuration[Evironments._PROMISEPOOl_]
    
    @property
    def logging(self) -> dict:
        return self._configuration[Evironments._LOGGING_]

    @property
    def deployment(self) -> list:
        return self._configuration[Evironments._DEPLOYMENT_]

    @property
    def redis(self) -> list:
        return self._configuration[Evironments._REDIS_]

    @property
    def database(self) -> dict:
        return self._configuration[Evironments._DATABASE_]

    @property
    def plugins(self) -> dict:
        plugin_profiles = dict()

        plugin_env = self._configuration[Evironments._PLUGINS_]
        incld_dir = plugin_env[Evironments._PLUGIN_INCLUDES_]

        try:

            # for file_name in listdir(self.conf_uri):
            #     if file_name.startswith(r'.') or (file_name.startswith(r'__') and file_name.endswith(r'__')):
            #         continue

            #     file_path = joinpath(xl_dir, file_name)
            #     if isfile(file_path):
            #         if is_xl_file(file_name):
            #             with open(file_path, 'rb') as fd:
            #                 yield fd, file_name
            #         elif is_csv_file(file_path):
            #             with open(file_path, 'rt', encoding='ansi') as fd:
            #                 yield fd, file_name
            #         elif is_zip_file(file_path):
            #             yield from xls_in_zip(file_path)

            #     elif isdir(file_path):
            #         yield from xls_in_dir(file_path)

            #     else:
            #         print(f" {file_name} 不是 xl、zip文件或文件夹，已忽略。")
            #         continue

            for path in (f for f in Path(Path(self.conf_uri).parent, incld_dir).rglob('**/*') if f.is_file()):
                with open(path.absolute(), "rb") as f:
                    profile = load(f)
                    plugin_profiles.update(profile)
        except FileNotFoundError as error:
            raise ConfigFileError(f"Could not read Config file. {error}")
        except Exception as error:
            raise ConfigContentError(f"Config file conatins invalid contents or missing permanent records. {error}")
        
        return plugin_profiles
    
