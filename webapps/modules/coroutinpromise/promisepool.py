
from collections import namedtuple

from webapps.language.decorators.singleton import singleton
from webapps.language.errors.enverror import ConfigContentError

from webapps.language.errors.promiseerror import PromiseIdentifierSame, PromisePoolOccupied
from webapps.modules.coroutinpromise.promise import Promise
from webapps.modules.coroutinpromise.promiseidentifier import PromiseIdentifier






@singleton
class PromisePool(object):

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
    
    def set_promise(self, promise, identifier: PromiseIdentifier):
        try:
            channel = self.channels[identifier.channel]
            channel[identifier.name] = promise

            self.registry[identifier.id] = promise
        except BaseException as error:
            raise error
    
    def require_promise(self, identifier: PromiseIdentifier):

        if identifier.channel not in self.channels:
            raise ConfigContentError("No channel named: {} found in configuration file.".format(identifier.channel))
        
        local_promise = self.registry[identifier.id]
        local_promise.done = True

        promise = Promise(identifier, local_promise.corofunc, identifier)
        self.set_promise(promise, identifier)

        return promise

    def make_the_promise(self, identifier: PromiseIdentifier):
        try:
            promise = self.channels[identifier.channel].pop(identifier.name)
        except KeyError as error:
            # __timber.critial()
            pass

        if identifier.id in self.registry:
            raise PromiseIdentifierSame()
        
        self.registry[identifier.id] = promise

        return promise
     
    @staticmethod
    def for_promise(corofunc, identifier: PromiseIdentifier):
        return PromisePool().require_promise(corofunc, identifier)
    

    @staticmethod
    def require(identifier: PromiseIdentifier):

        def decorator(func):

            async def decroration(*args, **kwargs) :

                await PromisePool.for_promise(func(), identifier)
            
            return decroration
        
        return decorator

    @staticmethod
    def deliver(identifier: PromiseIdentifier):

        def decorator(func):

            async def decroration(*args, **kwargs) :

                await PromisePool.for_promise(func(), identifier)
            
            return decroration
        
        return decorator
