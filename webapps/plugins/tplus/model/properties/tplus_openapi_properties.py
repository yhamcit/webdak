

from typing import Generator
from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties


@Singleton
class TplusOpenApiProperties(PluginClassProperties):

    _BASE_URL_    = "BaseUrl"
    _APP_KEY_     = "appKey"
    _APP_SECRET_  = "appSecret"
    _CIPHER_KEY_  = "cipherKey"
    _CERTIFICATE_ = "certificate"

    def __init__(self, name: str = None, valueset: dict = None) -> None:
        super().__init__(name, valueset)
     
    @property
    def valueset(self) -> dict:
        return self._valueset
    
    @valueset.setter
    def valueset(self, valueset: dict):
        self._valueset = valueset
     
    @property
    def base_url(self) -> str:
        return self._valueset[TplusOpenApiProperties._BASE_URL_]
        
    @property
    def app_key(self) -> str:
        return self._valueset[TplusOpenApiProperties._APP_KEY_]
        
    @property
    def app_secret(self) -> str:
        return self._valueset[TplusOpenApiProperties._APP_SECRET_]
        
    @property
    def cipher_key(self) -> str:
        return self._valueset[TplusOpenApiProperties._CIPHER_KEY_]
        
    @property
    def certificate(self) -> str:
        return self._valueset[TplusOpenApiProperties._CERTIFICATE_]


