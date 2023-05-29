

class TplusException(Exception):
    pass

class AppTicketNotAvialable(TplusException):
    pass

class AppTicketExpired(TplusException):
    pass
