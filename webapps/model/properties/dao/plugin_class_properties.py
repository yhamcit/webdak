

class PluginClassProperties(object):

    _PACKAGE_NAME_  = "Package"
    _CLASS_NAME_    = "Class"
    _URL_PREFIX_    = "urlPrefix"
    _ENDPOINTS_     = "endpoints"

    def __init__(self, name: str = None, valueset: dict = None):

        if not hasattr(self, "_name") or self._name != name:
            self._name = name

        if not hasattr(self, "_valueset"):
            self._valueset = None

        if self._valueset is not valueset:
            self.valueset = valueset
     
    @property
    def valueset(self) -> dict:
        return self._valueset

    @valueset.setter
    def valueset(self, valueset: dict):
        self._valueset = valueset
     
    @property
    def name(self) -> dict:
        return self._name
     
    @property
    def package_name(self) -> dict:
        return self._valueset[PluginClassProperties._PACKAGE_NAME_]
     
    @property
    def class_name(self) -> dict:
        return self._valueset[PluginClassProperties._CLASS_NAME_]
     
    @property
    def url_prefix(self) -> dict:
        return self._valueset[PluginClassProperties._URL_PREFIX_]

    @property
    def plugin_qualifier(self) -> str:
        return PluginClassProperties.make_qualifier(
            self._valueset[PluginClassProperties._PACKAGE_NAME_], 
            self._valueset[PluginClassProperties._CLASS_NAME_])
    
    @property
    def endpoint_profiles(self) -> tuple:
        return self._valueset[PluginClassProperties._ENDPOINTS_]

    @staticmethod
    def make_qualifier(pn, cn) -> str:
        return ".".join((pn.strip("."), cn.strip(".")))


