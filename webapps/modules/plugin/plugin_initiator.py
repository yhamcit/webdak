
from importlib import import_module

from re import compile

from quart import Quart

from webapps.model.properties.environments import Evironments
from webapps.model.properties.dao.plugin_environment import PluginEnvironment
from webapps.modules.plugin.plugin_blueprint import PluginBlueprint


class PluginInitiator(object):

    _PLUGIN_ROOT_ = "plugins"

    _IS_RELATIVE_MODULE_PATTERN_ = compile("^(?:\.+[a-zA-Z0-9_]+)+$")

    def __init__(self) -> None:
        self._plugin_env = PluginEnvironment(Evironments().plugins)
        self._blueprints = dict()

    def init_plugins(self):
        for props in self._plugin_env.properites():

            try:
                plugin_module = import_module(props.package_name)
                plugin_cls = getattr(plugin_module, props.class_name)
                plugin = plugin_cls(props.class_name, props)

                self.register_plugin(props, plugin)
            except Exception as error:
                raise EnvironmentError(error)

        return self

    def register_plugin(self, props, plugin):

        blueprint = PluginBlueprint(props)

        for endpoint in plugin.endpoints():
            blueprint.register_endpoints(endpoint)

        self._blueprints[props.plugin_qualifier] = blueprint
        return self

    def install(self, app: Quart):

        for bp in self._blueprints.values():
            app.register_blueprint(bp)

        return self

    @property
    def environment(self) -> dict:
        return self._plugin_env

