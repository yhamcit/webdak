

from typing import Any
from webapps.language.decorators.singleton import Singleton
from webapps.model.auth.access.access_errors import SerializableObjectNotAvialable

from webapps.model.identifier import ModelIdentifier


@Singleton
class SerializableObjectDepot(object):

    def __init__(self) -> None:
        self._vault = dict()


    def get(self, identifier: ModelIdentifier) -> Any:

        if identifier not in self._vault:
            raise SerializableObjectNotAvialable("Serializable object not found", f"{identifier} not found in depot.")
        
        return self._vault[identifier]


    def put(self, serializable: Any, identifier: ModelIdentifier) -> None:

        if not isinstance(serializable, str):
            serialization = str(serializable)

        if identifier in self._vault:
            SerializableObjectDepot._timber.debug("Serializable object updated", f"overwrite key: {serialization}")

        self._vault[identifier] = serialization
