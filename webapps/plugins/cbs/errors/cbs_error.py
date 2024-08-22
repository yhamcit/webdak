
class CBSException(BaseException):
    pass

class CBSProfileException(CBSException):
    pass

class ServerRejection(CBSException):
    pass

class UpstreamServiceError(CBSException):
    pass

class AppTokenExpired(CBSException):
    pass

class AppTokenInvalid(CBSException):
    pass

