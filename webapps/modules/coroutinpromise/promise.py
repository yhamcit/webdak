




from typing import Coroutine, Generator


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
    def __init__(self, identifier: str, coroutine: Coroutine) -> None:
        self._indentifier = identifier
        self._await_like = coroutine
        self._coro_switcher = None
        self._done_value = None

    def __await__(self):
        return self
    
    def __next__(self):
        self._then_value = yield
        return self._coro_switcher
    
    def __anext__ (self):
        pass

    __iter__ = __await__

    def send(self, value):
        pass

    def throw(self, error):
        pass

    def asend(self, value):
        pass

    def athrow(self, error):
        pass
    
    def delivery(self):
        self.coro_switcher = self.coro_switcher()
        self.coro_switcher.send(None)

    def coro_switcher(self):
        yield
        self.resolve(self._await_like)

    @property 
    def identifier(self) -> str:
        return self._identifier

    @property
    def coro_switcher(self):
        return self._coro_switcher
    
    @coro_switcher.setter
    def coro_switcher(self, switcher: Generator):
        self._coro_switcher = switcher