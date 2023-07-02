

class TplusException(Exception):
    pass

class AppTicketNotAvialable(TplusException):
    pass

class AppTicketExpired(TplusException):
    pass

class AppTokenUninitialized(TplusException):
    pass

class AppTokenExpired(TplusException):
    pass

class AppTicketRequestReject(TplusException):
    pass

class AppTicketRejectedByServer(TplusException):
    pass
