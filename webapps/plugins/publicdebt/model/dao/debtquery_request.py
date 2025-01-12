

class DebtQueryRequest():

    _REQUEST_HEADER_CONTENT_TYPE_ = "Content-Type"

    def __init__(self, valueset: dict) -> None:
        self.__dict__.update(valueset)
