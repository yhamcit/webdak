

from abc import abstractmethod

from webapps.modules.requests.httpheaders import HttpHeaders


class HttpHeadHandler(object):


    def __init__(self) -> None:
        pass

    @abstractmethod
    def pickup_headers(self, headers: HttpHeaders) -> HttpHeaders:
        pass

