

class TplusMsgActuator(object):

    __ID__          = "id"
    __APP_KEY__     = "appKey"
    __MSG_TYPE__    = "msgType"
    __TIME__        = "time"
    __BIZ_CONTENT__ = "bizContent"
    
    def __init__(self) -> None:
        self._hadler_registry = dict()

    def handle_msg(self, msg: dict) -> dict:
        msg_type = msg[TplusMsgActuator.__MSG_TYPE__]
        registry = self.handler_registry

        if msg_type in registry:
            return registry[msg_type].handle_msg(msg_type)
        
    def register(self, id: str, actuator) -> None:
        self.handler_registry[id] = actuator
    
    @property
    def handler_registry(self) -> dict:
        return self._hadler_registry