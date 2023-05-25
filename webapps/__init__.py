import sys
from os.path import abspath

from webapps.modules.lumber.lumber import Lumber


# for loc_path in __path__:
#     sys.path.append(abspath(loc_path))

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

__timber.info("System boot. Initializing actors.")

from webapps.actors.actorinitiator import ActorInitiator
ActorInitiator() \
    .init_actors() \
    .boot()
