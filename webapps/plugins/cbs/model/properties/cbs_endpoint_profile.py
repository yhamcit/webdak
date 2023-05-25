

from webapps.model.properties.dao.endpoint_profile import EndpointProfile
from webapps.plugins.cbs.model.properties.cbs_openapi_properties import CBSOpenApiProperties

class CBSEndpointProfile(EndpointProfile):

    _NAME_      = "name"
    _ID_        = "id"
    _PACKAGE_   = "Package"
    _CLASS_     = "Class"

    def __init__(self, valueset: dict, props: CBSOpenApiProperties) -> None:
        super().__init__(valueset, props)
        self._valueset = valueset
    
    @property
    def valueset(self):
        return self._valueset
