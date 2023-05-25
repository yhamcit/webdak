

from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties


@Singleton
class CBSOpenApiProperties(PluginClassProperties):

    _BASE_URL_              = "BaseUrl"
    _APP_ID_                = "appId"
    _APP_SECRET_            = "appSecret"
    _PRIVATE_CIPHER_KEY_    = "privateCipherKey"
    _PUBLIC_CIPHER_KEY_     = "publicCipherKey"

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
        return self._valueset[CBSOpenApiProperties._BASE_URL_]
        
    @property
    def app_id(self) -> str:
        return self._valueset[CBSOpenApiProperties._APP_ID_]
        
    @property
    def app_secret(self) -> str:
        return self._valueset[CBSOpenApiProperties._APP_SECRET_]

    @property
    def private_cipher_key(self) -> str:
        return self._valueset[CBSOpenApiProperties._PRIVATE_CIPHER_KEY_]

    @property
    def public_cipher_key(self) -> str:
        return self._valueset[CBSOpenApiProperties._PUBLIC_CIPHER_KEY_]

    @property
    def endpoint_profiles(self) -> tuple:
        return self._valueset[PluginClassProperties._ENDPOINTS_]
