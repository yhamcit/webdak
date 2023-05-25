from typing import Generator

from importlib import import_module

import json

from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties
from webapps.modules.plugin.endpoints import PluginEndpoint

from webapps.modules.plugin.plugin import Plugin
from webapps.plugins.tplus.model.properties.tplus_endpoint_profile import TplusEndpointProfile
from webapps.plugins.tplus.model.properties.tplus_openapi_properties import TplusOpenApiProperties

class TplusPlugin(Plugin):
    
    _SUCCESS_     = {"result": "success"}
    _FAILURE_     = {"result": "failed"}, 406

    def __init__(self, name: str, props: PluginClassProperties) -> None:
        super().__init__()
        self._name = name
        self._props = TplusOpenApiProperties(name, props.valueset)

    def endpoints(self) -> Generator[PluginEndpoint, None, None]:

        for profile in (TplusEndpointProfile(valueset, self._props) for valueset in self._props.endpoint_profiles):
            ep_module = import_module(profile.package_name)
            ep_cls = getattr(ep_module, profile.class_name)
            yield ep_cls(profile.name, profile, self._props)

    @staticmethod
    def success():
        return json.dumps(TplusPlugin._SUCCESS_)

    @staticmethod
    def failure():
        return json.dumps(TplusPlugin._FAILURE_)
