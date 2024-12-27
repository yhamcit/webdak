
from webapps.ingress import app

from webapps.modules.lumber.lumber import Lumber
from webapps.model.model_initiator import ModelInitiator
from webapps.core_initiator import SystemInitiator
from webapps.modules.plugin.plugin_initiator import PluginInitiator


_timber = Lumber.timber("root")
_timber.info("System boot. Initializing system components.")


ModelInitiator().ready()

SystemInitiator() \
    .boot()

_timber.info("System boot. Initializing actuators.")

PluginInitiator() \
    .init_plugins() \
    .install(app)
