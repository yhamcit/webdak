class AppTokenErrorDescription(object):
    _CODE_    = "code"
    _MSG_     = "msg"
    _HINT_    = "hint"

    def __init__(self, error_des: dict) -> None:
        self._raw = None

        self._code = ''
        self._msg = ''
        self._hint = ''

        if error_des:
            self.errors = error_des

    @property
    def code(self) -> str:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def hint(self) -> str:
        return self._hint

    @property
    def errors(self) -> dict:
        return self._raw

    @errors.setter
    def errors(self, error_des: dict) -> None:
        if AppTokenErrorDescription._CODE_ in error_des:
            self._code = error_des[AppTokenErrorDescription._CODE_]

        if AppTokenErrorDescription._MSG_ in error_des:
            self._msg = error_des[AppTokenErrorDescription._MSG_]

        if AppTokenErrorDescription._HINT_ in error_des:
            self._hint = error_des[AppTokenErrorDescription._HINT_]
    
