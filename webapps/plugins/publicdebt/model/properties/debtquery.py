

from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.endpoint_profile import EndpointProfile
from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties


@Singleton
class DebtQueryProperties(PluginClassProperties):

    def __init__(self, name: str = None, valueset: dict = None) -> None:
        super().__init__(name, valueset)
     
    @property
    def valueset(self) -> dict:
        return self._valueset
    
    @valueset.setter
    def valueset(self, valueset: dict):
        self._valueset = valueset

    @property
    def endpoint_profiles(self) -> tuple:
        return self._valueset[PluginClassProperties._ENDPOINTS_]




class DebtQueryProfile(EndpointProfile):

    _NAME_      = "name"
    _ID_        = "id"
    _PACKAGE_   = "Package"
    _CLASS_     = "Class"

    def __init__(self, valueset: dict, props: DebtQueryProperties) -> None:
        super().__init__(valueset, props)
        self._valueset = valueset
    
    @property
    def valueset(self):
        return self._valueset
