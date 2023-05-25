
from webapps.ingress import app

from webapps.modules.lumber.lumber import Lumber
from webapps.model.model_initiator import ModelInitiator
from webapps.core_initiator import SystemInitiator
from webapps.modules.plugin.plugin_initiator import PluginInitiator


_timber = Lumber.timber("root")
_timber.info("System boot. Initializing system components.")


ModelInitiator() \
    .init_database_connection() \
    .init_redis_connection() \
    .boot()


SystemInitiator() \
    .init_promise_pool() \
    .boot()

_timber.info("System boot. Initializing actuators.")

PluginInitiator() \
    .init_plugins() \
    .install(app)
