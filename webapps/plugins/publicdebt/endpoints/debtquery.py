from typing import Any

from quart import ResponseReturnValue, request as view_request
from quart.views import View

from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.modules.lumber.lumber import Lumber
from webapps.modules.requests.httpheaderpod import HttpHeaderPod
from webapps.plugins.publicdebt.model.dao.debtquery_request import DebtQueryRequest
from webapps.plugins.publicdebt.model.properties.debtquery import DebtQueryProfile, DebtQueryProperties

from webapps.plugins.sqlitedb.core import SqlitePlugin



class PublicDebtQuery(PluginEndpoint):

    _timber = Lumber.timber("public_debt")
    _err_timber = Lumber.timber("error")


    class DebtView(View):

        methods = ["GET", "POST"]

        def __init__(self, endpoint: PluginEndpoint) -> None:
            super().__init__()
            self._endpoint = endpoint

        async def dispatch_request(self, **kwargs: Any) -> ResponseReturnValue:

            if not DebtQueryRequest._REQUEST_HEADER_CONTENT_TYPE_ in view_request.headers:
                return "A valid request must contain specified: 'Content-Type' as 'application/json'."

            content_type = view_request.headers.get(DebtQueryRequest._REQUEST_HEADER_CONTENT_TYPE_)
            if (content_type != HttpHeaderPod._HDV_MIME_JSON_):
                return 'Content-Type not supported!'

            try:
                request = DebtQueryRequest(await view_request.get_json())
                return await self._endpoint.request(request.body)      
            except Exception as error:
                return f"Request data can not be processed, reason: {error} - {str(error.args)}", 406


    @property
    def view(self):
        return PublicDebtQuery.DebtView.as_view(self._profile.name, self)



    def __init__(self, name: str, profile: DebtQueryProfile, props: DebtQueryProperties) -> None:
        super().__init__(name, profile)

        self._profile = profile
        self._props = props
        self._conf_vault = dict()



    async def request(self, json_body: dict):

        return await self.do_request(json_body)



    async def do_request(self, json_body: dict):

        response = None

        sqlite = SqlitePlugin()
        result = await sqlite.query_debt()

        return response
