
from webapps.language.decorators.singleton import singleton


@singleton
class ActorGroup(object):

    def __init__(self) -> None:
        self._actor_vault = dict()

    def register_actor(self, id, actor) -> None:
        # TODO: verify actor
        self._actor_vault[id] = actor