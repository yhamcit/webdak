
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

    __timber = Lumber.timber("webdak")

    def __init__(self, channel_list: tuple) -> None:
        self._channels = dict(((name, dict()) for name in channel_list))
        self._registry = dict()

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

    def get_channel(self, identifier: PromiseIdentifier) -> dict:
        return self.channels[identifier.channel]
    
    def set_promise(self, promise: Promise, identifier: PromiseIdentifier) -> None:
        try:
            channel = self.channels[identifier.channel]
            channel[identifier.name] = promise

            self.registry[identifier.id] = promise
        except BaseException as error:
            raise error
        
    def the_promise(self, identifier: PromiseIdentifier, value: Any):
        if not self.has_channel(identifier):
            raise ConfigContentError("No channel named: {} found in configuration file.".format(identifier.channel))
        
        channel = self.get_channel(identifier)
        if identifier.name in channel:
            raise PromisePoolOccupied()

        promise = Promise(identifier)
        self.set_promise(promise, identifier)

        return promise
    
    def make_promise(self, identifier: PromiseIdentifier):
        try:
            promise = self.channels[identifier.channel].pop(identifier.name)

            if identifier.id in self.registry:
                raise PromiseIdentifierSame()
            
            self.registry[identifier.id] = promise

            return promise
        except KeyError as error:
            PromisePool.__timber.critial(f"Promise not found: {identifier.name}")
            return None

     
    @staticmethod
    def for_promise(identifier: PromiseIdentifier, value: Any):

        return PromisePool().the_promise(identifier, value)
     
    @staticmethod
    def deliver(identifier: PromiseIdentifier):

        return PromisePool().make_promise(identifier)
     
    # @staticmethod
    # def require(identifier: PromiseIdentifier):

    #     def decorator(func):

    #         @wraps(func)
    #         async def decroration(*args, **kwargs) :
    #             PromisePool.__timber.error(f"{identifier.channel}: {identifier.name} @ {identifier.id}")

    #             await func()
            
    #         return decroration
        
    #     return decorator

    # @staticmethod
    # def deliver(identifier: PromiseIdentifier):

    #     def decorator(func):

    #         @wraps(func)
    #         async def decroration(*args, **kwargs) :
    #             PromisePool.__timber.error(f"{identifier.channel}: {identifier.name} @ {identifier.id}")

    #             await func()
            
    #         return decroration
        
    #     return decorator

    @staticmethod
    def BBBB(identifier: PromiseIdentifier):



        return PromisePool().bbb(identifier)

    @staticmethod
    def Promise(identifier: PromiseIdentifier):

        def decorator(func):

            @wraps(func)
            async def decroration(*args, **kwargs) :
                PromisePool.__timber.error(f"{identifier.channel}: {identifier.name} @ {identifier.id}")

                corofunc = func()

                PromisePool.aaa(corofunc, identifier)

                await corofunc
            
            return decroration
        
        return decorator
