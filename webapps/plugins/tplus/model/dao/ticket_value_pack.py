

from webapps.plugins.tplus.model.dao.tplus_errors import TplusPushMsgException


class AppTicketValuePack():

    _TICKET_        = "appTicket"
    _TOKEN_TYPE_    = "token_type"
    _EXPIRES_       = "expires"

    def __init__(self, valueset: dict) -> None:
        try:
            self._ticket = valueset[AppTicketValuePack._TICKET_]
        except KeyError as error:
            raise TplusPushMsgException(f"{error}")

    @property
    def ticket(self) -> str:
        return self._ticket
