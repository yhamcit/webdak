
class HttpHeaders(object):

    __CHARSET__ = "Accept-Charset"

    def __init__(self, defaults = {__CHARSET__: "utf-8, iso-8859-1; q=1"}) -> None:
        self._header_vault = dict()

        self.header_vault |= defaults
    
    @property
    def header_vault(self) -> dict:
        return self._header_vault
    
    @header_vault.setter
    def header_vault(self, headers: dict) -> dict:
        self._header_vault = headers

    def update(self, headers: dict) -> None:
        self.header_vault |= headers

    def merge(self, headers: dict) -> dict:
        return self.header_vault | headers

