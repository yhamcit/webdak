

from webapps.language.decorators.singleton import singleton
from webapps.model.properties.dao.actorenvironment import ActorsEnvironment
from webapps.model.properties.dao.actorenvironment import ActorProfile


@singleton
class TplusOpenApiProfile(ActorProfile):

    __ACTOR__ = "actor"
    __APP_TICKET__ = "AppTicket"
    __APP_TOKEN__ = "AppToken"
    __CIPHER_KEY__ = "cipherKey"

    __ACTOR_PACKAGE__ = "ActorPackage"
    __ACTOR_CLASS__ = "ActorClass"

    __BASE_URL__ = "BaseUrl"
    __APP_KEY__ = "appKey"
    __APP_SECRET__ = "appSecret"
    __APP_TICKET__ = "appTicket"
    __APP_TOKEN__ = "accessToken"
    __API_PATH__ = "apiPath"
    __CERTIFICATE__ = "certificate"

    def __init__(self, name, profile) -> None:
        super().__init__(name, profile)
        self.profile = profile
        # self._actor_profile = None
        # self._app_ticket = None
        # self._app_token = None

    @property
    def profile(self) -> dict:
        return super().profile

    @profile.setter
    def profile(self, profile) -> None:
        super().set_profile(profile)
        self.actor_profile = profile[TplusOpenApiProfile.__ACTOR__]
        self.app_ticket = profile[TplusOpenApiProfile.__APP_TICKET__]
        self.app_token = profile[TplusOpenApiProfile.__APP_TOKEN__]

    @property
    def actor_profile(self) -> dict:
        return self._actor_profile

    @actor_profile.setter
    def actor_profile(self, actor_profile) -> None:
        self._actor_profile = actor_profile

    @property
    def app_ticket(self) -> dict:
        return self._app_ticket

    @app_ticket.setter
    def app_ticket(self, app_ticket) -> None:
        self._app_ticket = app_ticket

    @property
    def app_token(self) -> dict:
        return self._app_token

    @app_token.setter
    def app_token(self, app_token) -> None:
        self._app_token = app_token
    
    @property
    def actor_package_name(self) -> str:
        return self.actor_profile[TplusOpenApiProfile.__ACTOR_PACKAGE__]
    
    @property
    def actor_class_name(self) -> str:
        return self.actor_profile[TplusOpenApiProfile.__ACTOR_CLASS__]
    
    @property
    def actor_identifier(self) -> str:
        return ActorsEnvironment.make_identifier(
            self.actor_profile[TplusOpenApiProfile.__ACTOR_PACKAGE__], 
            self.actor_profile[TplusOpenApiProfile.__ACTOR_CLASS__])
     
    @property
    def base_url(self) -> str:
        return self.profile[TplusOpenApiProfile.__BASE_URL__]
        
    @property
    def app_key(self) -> str:
        return self.profile[TplusOpenApiProfile.__APP_KEY__]
        
    @property
    def app_secret(self) -> str:
        return self.profile[TplusOpenApiProfile.__APP_SECRET__]
        
    @property
    def cipher_key(self) -> str:
        return self.profile[TplusOpenApiProfile.__CIPHER_KEY__]

    @property
    def app_ticket_api_path(self) -> str:
        return self.app_ticket[TplusOpenApiProfile.__API_PATH__]
        
    @property
    def app_token_certifcate(self) -> str:
         return self.app_token[TplusOpenApiProfile.__CERTIFICATE__]
    
    @property
    def app_token_api_path(self) -> str:
        return self.app_token[TplusOpenApiProfile.__API_PATH__]

    