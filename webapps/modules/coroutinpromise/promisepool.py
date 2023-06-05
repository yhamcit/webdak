
import asyncio
from collections import namedtuple
from functools import wraps
from typing import Any, Coroutine

from webapps.language.decorators.singleton import singleton
from webapps.language.errors.enverror import ConfigContentError

from webapps.language.errors.promiseerror import PromiseIdentifierSame, PromisePoolOccupied
from webapps.modules.coroutinpromise.promise import Promise
from webapps.modules.coroutinpromise.promiseidentifier import PromiseIdentifier
from webapps.modules.lumber.lumber import Lumber





@singleton
class PromisePool(object):

    _timber = Lumber.timber("webdak")

    def __init__(self, channel_list: tuple) -> None:
        self._channels = dict(((name, dict()) for name in channel_list))

    @property
    def channels(self) :
        return self._channels

    @property
    def registry(self) :
        return self._registry

    @property
    def coroutine(self) :
        return self._wrapped_coroutine
    
    @coroutine.setter
    def coroutine(self, coro_func) :
        self._wrapped_coroutine = coro_func

    def has_channel(self, identifier: PromiseIdentifier) -> bool:
        return identifier.channel in self.channels

    def occupied(self, identifier: PromiseIdentifier) -> bool:
        return identifier.name in self.channels[identifier.channel]

    def get_channel(self, identifier: PromiseIdentifier) -> dict:
        return self.channels[identifier.channel]
    
    def the_promise(self, identifier: PromiseIdentifier, value: Any):
        if not self.has_channel(identifier):
            raise ConfigContentError(f"No channel named: {identifier.channel} found in configuration file.")
        
        if self.occupied(identifier):
            raise PromisePoolOccupied()

        try:
            promise = Promise(identifier)
            channel = self.channels[identifier.channel]
            channel[identifier.name] = promise
            PromisePool._timber.critical(f"PromisePools {self}")
            PromisePool._timber.critical(f"channels: {self.channels}, Promises: {self.channels[identifier.channel]}")

            return promise
        except Exception as error:
            PromisePool._timber.critical(f"error: {error}")
            raise error
    
    def make_promise(self, identifier: PromiseIdentifier):
        try:
            promise = self.channels[identifier.channel].pop(identifier.name)

            return promise
        except KeyError as error:
            PromisePool._timber.critical(f"PromisePools {self}")
            PromisePool._timber.critical(f"channels: {self.channels}, Promises: {self.channels[identifier.channel]}")
            PromisePool._timber.critical(f"Promise not found: {identifier.name}")
            return None

     
    @staticmethod
    def for_promise(identifier: PromiseIdentifier, value: Any):

        return PromisePool().the_promise(identifier, value)
     
    @staticmethod
    def deliver(identifier: PromiseIdentifier, value: Any):

        promise = PromisePool().make_promise(identifier)

        if promise is not None:
            promise.set_result(value)

        return promise
