
from collections import deque
from typing import Any, Coroutine, Iterable


from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.env_errors import ConfigContentError
from webapps.modules.coroutinpromise.dao.promise_errors import PromiseChannelNotExist, PromiseNotMade, PromisePoolCollapse

from webapps.modules.coroutinpromise.promise import Promise
from webapps.model.identifier import ModelIdentifier
from webapps.modules.lumber.lumber import Lumber





@Singleton
class PromisePool(object):

    _timber = Lumber.timber("webdak")

    def __init__(self) -> None:
        self._channels = dict()

    # @property
    # def registry(self) :
    #     return self._registry

    @property
    def coroutine(self) -> Coroutine:
        return self._wrapped_coroutine
    
    @coroutine.setter
    def coroutine(self, coro_func: Coroutine) :
        self._wrapped_coroutine = coro_func

    def has_channel(self, identifier: ModelIdentifier) -> bool:
        return identifier.channel in self._channels

    # def occupied(self, identifier: PromiseIdentifier) -> bool:
    #     return identifier.name in self._channels[identifier.channel]

    # def get_channel(self, identifier: PromiseIdentifier) -> dict:
    #     return self._channels[identifier.channel]
    
    def subscribe(self, identifiers: Iterable[ModelIdentifier]) -> None:
        channel = dict()

        for identifier in identifiers:
            if identifier.channel not in self._channels:
                self._channels[identifier.channel] = dict()
            
            channel = self._channels[identifier.channel]

            if identifier.name not in channel:
                channel[identifier.name] = deque()
    
    def fetch_promise(self, identifier: ModelIdentifier, value: Any=None, pop: bool=False) -> Promise:
        try:
            channel = self._channels[identifier.channel]
        except KeyError as error:
            raise PromiseChannelNotExist(error)

        try: 
            line = channel[identifier.name]
        except KeyError as error:
            raise PromisePoolCollapse(error)

        promise = line.popleft()
        
        if not promise:
            raise PromiseNotMade(f"No promise found in queue: {identifier.channel}:{identifier.name}")
        
        if not pop:
            line.appendleft(promise)
        
        return promise
    
    def put_promise(self, identifier: ModelIdentifier):
        if not self.has_channel(identifier):
            raise PromiseChannelNotExist(f"Channel named '{identifier.channel}' is not been subscribed.")

        try:
            promise = Promise(identifier)
            channel = self._channels[identifier.channel]
            line = channel[identifier.name]
            line.append(promise)

            return promise
        except KeyError as error:
            raise PromisePoolCollapse(error)
        
    @staticmethod
    def subscribe_channel(identifiers: Iterable[ModelIdentifier]) -> None:
        PromisePool().subscribe(identifiers)

    @staticmethod
    def OBSOLETED_make_promise(identifier: ModelIdentifier):
        try:
            return PromisePool().put_promise(identifier)
        except PromisePoolCollapse as error:
            PromisePool._timber.critical(f"Promise queue '{identifier.name}' on channel '{identifier.channel}' is not proper initialized.")
            raise error
        except IndexError as error:
            PromisePool._timber.critical(f"{error}")
        except Exception as error:
            PromisePool._timber.critical(f"{error}")
            raise error
     
    @staticmethod
    def wish(identifier: ModelIdentifier, value: Any):
        try:
            return PromisePool().put_promise(identifier)
        except (PromisePoolCollapse, IndexError) as error:
            PromisePool._timber.critical(f"Promise queue '{identifier.name}' on channel '{identifier.channel}' is not proper initialized.")
            raise error
        except Exception as error:
            PromisePool._timber.critical(f"Unexpect error: {error} - {error.args}")
            raise error

    @staticmethod
    def promise(identifier: ModelIdentifier, value: Any):

        try:
            promise = PromisePool().fetch_promise(identifier, pop = True)
            promise.set_result(value)
        except (PromiseChannelNotExist, PromisePoolCollapse) as error:
            PromisePool._timber.critical(f"Channels: {identifier.channel} not exist or queue {identifier.name} is not proper initialized.")
            raise error
        except PromiseNotMade as error:
            PromisePool._timber.critical("No need to fulfill: no object is waiting on the promise <{identifier.channel}>:<{identifier.name}>")
        except IndexError as error:
            PromisePool._timber.critical(f"{error}")
        except Exception as error:
            PromisePool._timber.critical(f"{error}")
            raise error
