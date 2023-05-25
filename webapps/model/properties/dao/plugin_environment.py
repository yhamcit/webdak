
from typing import Generator
from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties


@Singleton
class PluginEnvironment(object):
    def __init__(self, valueset: dict):
        self._properties_vault = dict()
        self._valueset = valueset

    def properites(self) -> Generator:
        return (PluginClassProperties(name, valueset) for name, valueset in self._valueset.items())
    
    def register_props(self, id: str, properties: PluginClassProperties):
        self._properties_vault[id] = properties
