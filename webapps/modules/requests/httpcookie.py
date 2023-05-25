
from http.cookiejar import CookieJar

from httpx import Cookies



class HttpCookieJar(CookieJar):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)



class HttpCookie(Cookies):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @property
    def cookiejar(self) -> HttpCookieJar:
        return self.jar

