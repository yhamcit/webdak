
import json

from typing import Any

from quart import ResponseReturnValue, request as view_request
from quart.views import View



from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.modules.lumber.lumber import Lumber
from webapps.plugins.publicdebt.model.dao.tables import LocalPublicDebt
from webapps.plugins.publicdebt.model.properties.debtquery import DebtQueryProfile, DebtQueryProperties





class PublicDebtQuery(PluginEndpoint):

    _timber = Lumber.timber("public_debt")
    _err_timber = Lumber.timber("error")


    class BrokerView(View):

        def __init__(self, endpoint: PluginEndpoint) -> None:
            super().__init__()
            self._endpoint = endpoint

        async def dispatch_request(self, **kwargs: Any) -> ResponseReturnValue:

            try:
                return await self._endpoint.request()      
            except Exception as error:
                PublicDebtQuery._err_timber.error(f"{error}", f"{error.args}")

                return f"Request data can not be processed, reason: {error} - {str(error.args)}", 406


    @property
    def view(self):
        return PublicDebtQuery.BrokerView.as_view(self._profile.name, self)



    def __init__(self, name: str, profile: DebtQueryProfile, props: DebtQueryProperties) -> None:
        super().__init__(name, profile)

        self._profile = profile
        self._props = props
        self._conf_vault = dict()
        # self._sqlitedb = db




    async def do_request(self, json_body: dict):

        response = None


        return response
