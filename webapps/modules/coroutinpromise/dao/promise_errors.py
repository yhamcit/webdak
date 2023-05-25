
class PromiseException(Exception):
    pass

class PromiseChannelNotExist(PromiseException):
    pass

class PromisePoolCollapse(PromiseException):
    pass

class PromiseNotMade(PromiseException):
    pass
