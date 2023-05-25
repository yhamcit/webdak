from time import time
from datetime import datetime

from webapps.language.errors.tpluserror import AppTicketExpired

class AppTicket(object):

    __TEN_MINUTES__ = 10 * 60

    __ENCRYPT_MSG__ = "encryptMsg"

    __MSG_TYPE__    = "msgType"
    __TIME_STAMP__  = "time"
    __BIZ_CONTENT__ = "bizContent"

    __APP_TICKET__  = "appTicket"

    def __init__(self, content: dict) -> None:
        self._json = content
        self._biz_content = self.json[AppTicket.__BIZ_CONTENT__]
        self._time_stamp = int(self.json[AppTicket.__TIME_STAMP__])

    @property
    async def app_ticket(self) -> str:
        if not self.be_valid:
            # TODO: rasie app ticket exception
            raise AppTicketExpired("App ticket has been expired.")

        return self._app_ticket
    
    @app_ticket.setter
    def app_ticket(self, new_token: str) -> None:
        self._app_ticket = new_token
        self._generated_time = time()

    @property
    def json(self) -> dict:
        return self._json

    @property
    def app_ticket(self) -> str:
        return self._biz_content[AppTicket.__APP_TICKET__]

    @property
    def time_stamp(self) -> int:
        return self._time_stamp

    @property
    def be_valid(self):
        if self._app_ticket:
            return (time() - self.time_stamp) >= AppTicket.__TEN_MINUTES__
        return False
    