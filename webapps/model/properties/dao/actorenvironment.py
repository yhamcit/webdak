

from webapps.language.decorators.singleton import singleton


@singleton
class ActorsEnvironment(object):

    def __init__(self):
        self._environment = dict()
        self._actor_profile_vault = dict()

    def __iter__(self) -> tuple:
        return (ActorProfile(name, actor_env) for name, actor_env in self._environment.items())
    
    @property
    def environment(self) -> dict:
        return self._environment
    
    @environment.setter
    def environment(self, actor_env):
        self._environment = actor_env

    def register_actor_profile(self, id, actor_profile) -> None:
        self._actor_profile_vault[id] = actor_profile

    def get_actor_profile(self, id):
        return self._actor_profile_vault[id]
    
    @staticmethod
    def make_identifier(pn, cn) -> str:
        return ".".join((pn, cn))


class ActorProfile(object):

    __MODEL_PACKAGE__ = "ModelPackage"
    __MODEL_CLASS__ = "ModelClass"

    def __init__(self, name: str, actor_profile: dict) -> None:
        self._name = name
        self._profile = actor_profile

    @property
    def name(self) -> str:
        return self._name

    @property
    def profile(self) -> dict:
        return self._profile

    @profile.setter
    def profile(self, profile) -> None:
        self._profile = profile

    def set_profile(self, profile) -> None:
        self._profile = profile

    @property
    def model_package_name(self) -> str:
        return self.profile[ActorProfile.__MODEL_PACKAGE__]
    
    @property
    def model_class_name(self) -> str:
        return self.profile[ActorProfile.__MODEL_CLASS__]
    
    @property
    def model_identifier(self) -> str:
        return ActorsEnvironment.make_identifier(
            self.profile[ActorProfile.__MODEL_PACKAGE__], 
            self.profile[ActorProfile.__MODEL_CLASS__])
