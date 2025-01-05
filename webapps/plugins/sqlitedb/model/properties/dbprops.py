

from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.endpoint_profile import EndpointProfile
from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties


@Singleton
class SqliteProperties():

    def __init__(self, valueset: dict = None) -> None:
        self.__dict__.update(valueset)
     
    @property
    def valueset(self) -> dict:
        return self._valueset
    
    @valueset.setter
    def valueset(self, valueset: dict):
        self._valueset = valueset
