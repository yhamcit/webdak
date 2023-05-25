

class HttpException(Exception):
    pass

class HttpSessionInitialized(HttpException):
    pass

class HttpInvalidUrl(HttpException):
    pass

class HttpInvalideHeaders(Exception):
    pass

class HttpServerReject(HttpException):
    pass

class HttpNetworkIssue(HttpException):
    pass

class HttpRequestReject(HttpException):
    pass
