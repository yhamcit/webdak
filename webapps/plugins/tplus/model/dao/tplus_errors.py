

class TplusException(BaseException):
    pass

class TplusPushMsgException(TplusException):
    pass

class AppTicketInvalid(TplusException):
    pass

class AppTicketExpired(TplusException):
    pass

class AppTokenUninitialized(TplusException):
    pass

class AppTokenExpired(TplusException):
    pass

class AppTokenInvalid(TplusException):
    pass

class AppTicketRequestReject(TplusException):
    pass

class AppTicketRejectedByServer(TplusException):
    pass

