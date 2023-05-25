
from abc import abstractmethod

from typing import Any, Coroutine

from quart import ResponseReturnValue
from quart.typing import ResponseReturnValue

from webapps.modules.plugin.dao.plugin_error import PluginProfileException

from webapps.model.properties.dao.endpoint_profile import EndpointProfile

class PluginEndpoint():

    def __init__(self, name: str, profile: EndpointProfile=None) -> None:

        if not profile:
            raise PluginProfileException("Can not initialze plugin endpoint objects with empty profile.")
        self._name = name
        self._profile = profile

    @property
    @abstractmethod
    def view(self):
        pass
    
    @property
    def url(self) -> str:
        return f"{self._profile.plugin_props.url_prefix.rstrip('/')}/{self._profile.route.strip('/')}"
