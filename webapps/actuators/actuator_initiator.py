
from importlib import import_module

from re import compile
from re import match
from webapps.actuators.actuator_group import ActuatorGroup

from webapps.model.properties.environments import Evironments
from webapps.model.properties.dao.actorenvironment import actuatorsEnvironment


class ActuatorInitiator(object):

    __IS_RELATIVE_MODULE_PATTERN__ = compile("^(?:\.+[a-zA-Z0-9_]+)+$")

    def __init__(self) -> None:
        self._actor_env = actuatorsEnvironment()
        self._actor_env.environment = Evironments().actuators

    def init_actuators(self):
        for base_actor_profile in self._actor_env:

            try:
                profile_module = import_module(base_actor_profile.model_package_name)
                profile_cls = getattr(profile_module, base_actor_profile.model_class_name)
                actuator_profile = profile_cls(base_actor_profile.name, base_actor_profile.profile)
            except Exception as error:
                raise EnvironmentError(error)
            
            self._actor_env.register_actor_profile(actuator_profile.actuator_identifier, 
                                                   actuator_profile)

            try:
                actuator_module = import_module(actuator_profile.actuator_package_name)
                actuator_cls = getattr(actuator_module, actuator_profile.actuator_class_name)
                actuator = actuator_cls(actuator_profile)
            except Exception as error:
                raise EnvironmentError(error)
            
            ActuatorGroup().register_actuator(actuator_profile.actuator_identifier, actuator)

        return self

    def boot(self):
        return self

    #     self._tplus_actor = AppTicketActor()

    # def init_app_ticket_executor(self):
    #     self._tplus_actor.renew_app_tiket()

        
