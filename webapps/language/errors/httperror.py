

class HttpException(Exception):
    pass

class HttpSessionInitialized(HttpException):
    pass

class HttpUrlNotValid(HttpException):
    pass

class HttpServerReject(HttpException):
    pass

class HttpNetworkIssue(HttpException):
    pass

class HttpRequestReject(HttpException):
    pass
