


class CBSRestfulapiBrokerRequest():

    _API_PATH_      = "api_path"
    _API_METHOD_    = "api_method"
    _BODY_          = "request_body"

    _REQUEST_HEADER_CONTENT_TYPE_ = "Content-Type"

    def __init__(self, valueset: dict) -> None:
        self._valueset = valueset

    @property
    def api_path(self) -> str:
        return self._valueset[CBSRestfulapiBrokerRequest._API_PATH_]
    

    @property
    def api_method(self) -> str:
        return self._valueset[CBSRestfulapiBrokerRequest._API_METHOD_]
    

    @property
    def body(self) -> dict:
        return self._valueset[CBSRestfulapiBrokerRequest._BODY_]
