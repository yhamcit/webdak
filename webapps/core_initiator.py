

from webapps.model.properties.environments import Evironments

class SystemInitiator(object):

    def __init__(self) -> None:
        self._app_env = Evironments()

    def boot(self) :
        return self

