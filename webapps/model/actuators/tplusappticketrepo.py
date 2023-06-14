

from webapps.endpoints.tplus.auth.appticket import AppTicket
from webapps.language.errors.tpluserror import AppTicketNotAvialable


class TplusAppTicketRepo(object):
    def __init__(self) -> None:
        self._ticket = None

    @property
    def ticket(self):
        if self._ticket is None:
            raise AppTicketNotAvialable()

        return self._ticket

    @ticket.setter
    def ticket(self, ticket: AppTicket) -> None:
        self._ticket = ticket
