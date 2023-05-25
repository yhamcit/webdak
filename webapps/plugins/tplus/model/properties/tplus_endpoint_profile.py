
from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.endpoint_profile import EndpointProfile
from webapps.plugins.tplus.model.properties.tplus_openapi_properties import TplusOpenApiProperties


class TplusEndpointProfile(EndpointProfile):

    _NAME_      = "name"
    _ID_        = "id"
    _PACKAGE_   = "Package"
    _CLASS_     = "Class"

    _APP_TICKET_  = "appTicket"
    _API_PATH_    = "apiPath"

    def __init__(self, valueset: dict, props: TplusOpenApiProperties) -> None:
        super().__init__(valueset, props)
        self._valueset = valueset
    
    @property
    def valueset(self):
        return self._valueset
