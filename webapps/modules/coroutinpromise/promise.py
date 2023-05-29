




from typing import Coroutine, Generator

from webapps.modules.coroutinpromise.promiseidentifier import PromiseIdentifier



class Promise(object):
    """
        Promise: Asynchronous Generator as communiction medium between corotinues

        coro_A : 
            # approch 1:
            in_value = proms.await_with(out_value)

            # approch 2:
            async for value in <promise>:
                # do something

            # approch 3:
            async with <promise> as proms:
                in_value = proms.await_with(out_value)

        coro_B :
            <promise>.send(values)

        coro_A :
            <continues>
    """
    def __init__(self, corofunc: Coroutine, identifier: PromiseIdentifier) -> None:
        self._corofunc = corofunc
        self._done = False
        self._indentifier = identifier

    def __await__(self):
        self.corofunc = self.corofunc()
        return self
    
    def __next__(self):
        self.corofunc.send(None)
    
    async def __anext__ (self):
        pass

    async def __aenter__(self):
        await print("IO operations")

    async def __aexit__(self, exc_type, exc, tb):
        await print("IO operations")

    __iter__ = __await__

    def send(self, value):
        pass

    def throw(self, error):
        pass

    def asend(self, value):
        pass

    def athrow(self, error):
        pass

    def corofunc(self):
        while self.done is not True:
            yield

    @property 
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, done: bool):
        self._done = done

    @property 
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        self._identifier = identifier

    @property
    def corofunc(self):
        return self._corofunc
    
    @corofunc.setter
    def corofunc(self, corofunc: Generator):
        self._corofunc = corofunc

    def resolve(self, value):
        try:
            return self.corofunc.send(value)
        except StopIteration as done:
            # __timber
            pass
        else:
            self.fullfill()

    def fullfill(self) -> None:
        pass