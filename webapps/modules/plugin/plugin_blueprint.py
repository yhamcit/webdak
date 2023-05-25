from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties

from quart import Blueprint

class PluginBlueprint(Blueprint):

    def __init__(self, props: PluginClassProperties) -> None:
        super().__init__(props.class_name, props.package_name, props.url_prefix)
        self._cls_props = props

    @property
    def manifests(self) -> PluginClassProperties:
        return self._cls_props

    @manifests.setter
    def manifests(self, props: PluginClassProperties):
        self._cls_props = props

    @property
    def properties(self) -> PluginClassProperties:
        return self._cls_props

    @properties.setter
    def properties(self, props: PluginClassProperties):
        self._cls_props = props

    def register_endpoints(self, endpoint):
        self.add_url_rule(endpoint.url, view_func = endpoint.view)
