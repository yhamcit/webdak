
from webapps.language.decorators.singleton import singleton


@singleton
class ActuatorGroup(object):

    def __init__(self) -> None:
        self._actor_vault = dict()

    def register_actuator(self, id, actor) -> None:
        # TODO: verify actor
        self._actor_vault[id] = actor