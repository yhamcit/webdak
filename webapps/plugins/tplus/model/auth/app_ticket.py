from time import time

import json

from webapps.plugins.tplus.model.dao.ticket_value_pack import AppTicketValuePack

from webapps.plugins.tplus.model.dao.tplus_errors import AppTicketExpired, AppTicketInvalid



class AppTicket(object):

    _TEN_SECONDS_       = 10
    _THIRTY_MINUTES_    = 30 * 60
    _ALIVE_LIFETIME_    = _THIRTY_MINUTES_ - _TEN_SECONDS_

    _ENCRYPT_MSG_       = "encryptMsg"
    _MSG_TYPE_          = "msgType"
    _TIME_STAMP_        = "time"
    _BIZ_CONTENT_       = "bizContent"
    _APP_TICKET_        = "appTicket"

    def __init__(self, value: (dict, str)) -> None:

        if isinstance(value, str):
            valueset = json.loads(value)
        elif isinstance(value, dict):
            valueset = value
        else:
            raise AppTicketInvalid(f"App Ticket must be one of (str, dict/json), got {type(value)} -{str(value)}")
        self._valueset = valueset

        if AppTicket._BIZ_CONTENT_ in valueset:
            self._value_pack = AppTicketValuePack(valueset[AppTicket._BIZ_CONTENT_])
        else:
            raise AppTicketInvalid(f"App Ticket must be one of (str, dict/json), got {type(value)} -{str(value)}")

        self._timestamp = int(self.valueset[AppTicket._TIME_STAMP_])

    def __str__(self) -> str:
        return json.dumps(self._valueset)

    @property
    async def valueset(self) -> str:
        if not self.be_valid:
            raise AppTicketExpired()

        return self._valueset
    
    @valueset.setter
    def valueset(self, new_token: str) -> None:
        self._valueset = new_token

    @property
    def valueset(self) -> dict:
        return self._valueset

    @property
    def ticket(self) -> str:
        return self._value_pack.ticket

    @property
    def timestamp(self) -> int:
        return self._timestamp
    
    @property
    def lifetime(self) -> int:
        return (int(time()) - self._timestamp)

    @property
    def is_valid(self):
        if self._value_pack:
            return self.lifetime <= AppTicket._ALIVE_LIFETIME_
        return False
    