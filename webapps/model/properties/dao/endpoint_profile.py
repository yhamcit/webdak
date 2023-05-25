from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties


class EndpointProfile(object):

    _PACKAGE_NAME_   = "Package"
    _CLASS_NAME_     = "Class"

    _NAME_  = "name"
    _ROUTE_ = "route"
    
    def __init__(self, valueset: dict, plugin_props: PluginClassProperties) -> None:
        self._valueset = valueset
        self._plugin_props = plugin_props

    @property
    def valueset(self) -> dict:
        return self._valueset

    @valueset.setter
    def valueset(self, valueset) -> None:
        self._valueset = valueset

    @property
    def plugin_props(self) -> dict:
        return self._plugin_props

    @plugin_props.setter
    def plugin_props(self, plugin_props) -> None:
        self._plugin_props = plugin_props

    @property
    def name(self) -> str:
        return self._valueset[EndpointProfile._NAME_]

    @property
    def route(self) -> str:
        return self._valueset[EndpointProfile._ROUTE_]

    @property
    def package_name(self) -> str:
        return self._valueset[EndpointProfile._PACKAGE_NAME_]
    
    @property
    def class_name(self) -> str:
        return self._valueset[EndpointProfile._CLASS_NAME_]

    @property
    def endpoint_qualifier(self) -> str:
        return EndpointProfile.make_qualifier(
            self._valueset[EndpointProfile._PACKAGE_NAME_], 
            self._valueset[EndpointProfile._CLASS_NAME_])

    @staticmethod
    def make_qualifier(pn, cn) -> str:
        return ".".join((pn.strip("."), cn.strip(".")))

