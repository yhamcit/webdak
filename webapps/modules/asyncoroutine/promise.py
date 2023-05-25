

from asyncio import Future


class Promise(Future):
    def __init__(self) -> None:
        self._generator = None
        self._then_value = None
        self._yield_value = None
        self._done_value = None

    # def __await__(self):
    #     def func_g():
    #         yield 
    #     self._generator = func_g()

    #     yield from self._generator

    #     return self._done_value
    
    # def __next__(self):
    #     self._then_value = yield
    #     return self._yield_value
    
    def resolve(self, value: any):
        self._generator.send(value)

    def reject(self, error: BaseException):
        pass

    def then(self, did_fullfill: lambda: None, did_rejected: lambda: None):
        pass

    # __iter__ = __await__
    