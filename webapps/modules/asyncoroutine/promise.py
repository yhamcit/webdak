

class Promise(object):
    def __init__(self) -> None:
        self._then_value = None
        self._yield_value = None
        self._done_value = None

    def __await__(self):
        self._then_value = yield self._yield_value
        return self._done_value
    
    def resolve(self, value: any):
        self.send(value)

    def reject(self, error: BaseException):
        pass

    def then(self, did_fullfill: lambda: None, did_rejected: lambda: None):
        pass

    __iter__ = __await__
    