

from typing import Any

from quart.views import View



from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.modules.lumber.lumber import Lumber





class SqliteHealthz():
    _timber = Lumber.timber("public_debt")
    _err_timber = Lumber.timber("error")


    class BrokerView(View):

        def __init__(self, endpoint: PluginEndpoint) -> None:
            super().__init__()
            self._endpoint = endpoint

        async def dispatch_request(self, **kwargs: Any) -> Any:

            return "OK", 200


    @property
    def view(self):
        return SqliteHealthz.BrokerView.as_view(self._profile.name, self)



    def __init__(self, name: str, profile: Any, props: Any) -> None:
        super().__init__(name, profile)

        self._profile = profile



    async def do_request(self, json_body: dict):

        response = None

        return response
