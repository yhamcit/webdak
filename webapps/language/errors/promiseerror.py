
class PromiseException(Exception):
    pass

class PromisePoolOccupied(PromiseException):
    pass

class PromiseIdentifierSame(PromiseException):
    pass
