
from types import GeneratorType
from typing import Awaitable
from webapps.language.decorators.singleton import singleton
from webapps.language.errors.enverror import ConfigContentError

from webapps.language.errors.promiseerror import PromisePoolOccupied
from webapps.modules.coroutinpromise.promise import Promise



@singleton
class PromisePool(object):

    def __init__(self, channel_list: tuple) -> None:
        self._channels = dict(((name, dict()) for name in channel_list))
        self._waitings = dict()
        self._wrapped_coroutine = lambda : None

    def __await__(self) -> Awaitable:
        return self
    
    __iter__ = __await__

    def __next__(self):

        if SomeConditionMatched:
            raise StopIteration("Coroutine suspended.")
        
        return self.coroutine.send()
    
    @property
    def channels(self) :
        return self._channels
    
    @property
    def waitings(self) :
        return self._waitings
    
    @property
    def coroutine(self) :
        return self._wrapped_coroutine
    
    @coroutine.setter
    def coroutine(self, coro_func) :
        self._wrapped_coroutine = coro_func
    
    def set_promise(self, promise, channel: str, name: str, identifier: str):
        try:
            ch = self.channels[channel]
            ch[name] = promise
        except BaseException as error:
            raise error
    
    def set_waitings(self, identifier: str, waiting: GeneratorType):
        try:
            self.waitings[identifier] = waiting
        except BaseException as error:
            raise error

    def require_promise(self, channel: str, name: str, identifier: str):

        if channel not in self.channels:
            raise ConfigContentError("No channel named: {} found in configuration file.".format(channel))

        promise = Promise(identifier)
        self.set_promise(promise, channel, name, identifier)

        return promise

    def make_the_promise(self, channel: str, name: str, identifier: str):
        channel = self.channels[channel]
        promise = Promise()

        try:
            followee_promise = channel[name]
            followee_promise.resolve(promise)
        except StopIteration as done:
            return promise
        else:
            # TODO: what exception
            raise Exception()

        return promise
    
    @staticmethod
    def the_promise(channel: str, name: str, id: str):

        PromisePool().require_promise(channel, name, id)

        return PromiseSolver()
