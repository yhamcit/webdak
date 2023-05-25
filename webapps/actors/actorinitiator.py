
from importlib import import_module

from re import compile
from re import match
from webapps.actors.actorgroup import ActorGroup

from webapps.model.properties.environments import Evironments
from webapps.model.properties.dao.actorenvironment import ActorsEnvironment


class ActorInitiator(object):

    __IS_RELATIVE_MODULE_PATTERN__ = compile("^(?:\.+[a-zA-Z0-9_]+)+$")

    def __init__(self) -> None:
        self._actor_env = ActorsEnvironment()
        self._actor_env.environment = Evironments().actors

    def init_actors(self):
        for base_actor_profile in self._actor_env:

            try:
                profile_module = import_module(base_actor_profile.model_package_name)
                profile_cls = getattr(profile_module, base_actor_profile.model_class_name)
                actor_profile = profile_cls(base_actor_profile.name, base_actor_profile.profile)
            except Exception as error:
                raise EnvironmentError(error)
            
            self._actor_env.register_actor_profile(actor_profile.actor_identifier, 
                                                   actor_profile)

            try:
                actor_module = import_module(actor_profile.actor_package_name)
                actor_cls = getattr(actor_module, actor_profile.actor_class_name)
                actor = actor_cls(actor_profile)
            except Exception as error:
                raise EnvironmentError(error)
            
            ActorGroup().register_actor(actor_profile.actor_identifier, actor)

        return self

    def boot(self):
        return self

    #     self._tplus_actor = AppTicketActor()

    # def init_app_ticket_executor(self):
    #     self._tplus_actor.renew_app_tiket()

        
