
from webapps.modules.lumber.lumber import Lumber


from webapps.model.modelinitiator import ModelInitiator
ModelInitiator() \
    .init_database_connection() \
    .init_redis_connection() \
    .boot()

__timber = Lumber.timber("root")

__timber.info("System boot. Initializing system components.")

from webapps.initiator import SystemInitiator
SystemInitiator() \
    .init_promise_pool() \
    .boot()

__timber.info("System boot. Initializing actuators.")

from webapps.actuators.actuator_initiator import ActuatorInitiator
ActuatorInitiator() \
    .init_actuators() \
    .boot()
