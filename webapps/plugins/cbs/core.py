from typing import Generator

from importlib import import_module

from webapps.language.decorators.singleton import Singleton

from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties

from webapps.modules.plugin.plugin import Plugin
from webapps.plugins.cbs.model.properties.cbs_endpoint_profile import CBSEndpointProfile
from webapps.plugins.cbs.model.properties.cbs_openapi_properties import CBSOpenApiProperties
from webapps.modules.plugin.endpoints import PluginEndpoint


@Singleton
class CBSPlugin(Plugin):

    def __init__(self, name: str, props: PluginClassProperties) -> None:
        super().__init__()
        self._name = name
        self._props = CBSOpenApiProperties(name, props.valueset)

    def endpoints(self) -> Generator[PluginEndpoint, None, None]:

        for profile in (CBSEndpointProfile(valueset, self._props) for valueset in self._props.endpoint_profiles):
            ep_module = import_module(profile.package_name)
            ep_cls = getattr(ep_module, profile.class_name)
            yield ep_cls(profile.name, profile, self._props)

