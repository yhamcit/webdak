

from typing import Any
from webapps.language.decorators.singleton import Singleton
from webapps.model.auth.access.access_errors import SerializableObjectNotAvialable

from webapps.modules.lumber.lumber import Lumber


@Singleton
class SerializableObjectDepot(object):

    _timber = Lumber.timber("model")

    def __init__(self) -> None:
        self._vault = dict()


    def get(self, identifier: str) -> Any:

        if identifier not in self._vault:
            raise SerializableObjectNotAvialable("Serializable object not found", f"{identifier} not found in depot.")
        
        return self._vault[identifier]


    def put(self, serializable: Any, identifier: str) -> None:

        if not isinstance(serializable, str):
            serialization = str(serializable)

        if identifier in self._vault:
            SerializableObjectDepot._timber.debug(f"Serializable object overwritten: {serialization}")

        self._vault[identifier] = serialization
