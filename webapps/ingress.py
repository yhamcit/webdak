
from flask import Flask, request
from webapps.actors.tplus.auth.appticketactor import AppTicketActor
from webapps.language.errors.tpluserror import AppTicketExpired, AppTicketNotAvialable
from webapps.model.properties.dao.actorenvironment import ActorsEnvironment

from webapps.model.properties.preference import Preference

from webapps.endpoints.tplus.auth.appticket import AppTicket
from webapps.modules.coroutinpromise.promisepool import PromisePool
from webapps.modules.coroutinpromise.promisepool import PromiseIdentifier

from webapps.modules.lumber.lumber import Lumber


__timber = Lumber.timber("root")


app = Flask(__name__)



app_tocken_actr_promise = PromiseIdentifier("tplus_actors_channel", "tplust_authen", "/actors/tplus/auth/appToken")
@app.route(app_tocken_actr_promise.id, methods=["GET", "POST"])
# @PromisePool.require(app_tocken_actr_promise)
async def actor_tplus_app_token():
    __timber.info(app_tocken_actr_promise.id)

    if request.method == "GET":
        try:
            app_token = await AppTicketActor().exchange_app_ticket()

            return app_token
        except AppTicketNotAvialable or AppTicketExpired as error:
            pass

    await AppTicketActor().renew_app_token()

    # await PromisePool.for_promise(app_tocken_actr_promise, None)

    async for app_ticket

    __timber = Lumber.timber("root")

    app_token = await AppTicketActor().exchange_app_ticket()
    
    return app_token


@app.route("/endpoints/healthz")
async def hello():
    __timber.info("/endpoints/tplus/auth/appToken")
    return "ok!"


app_ticket_ep_promise = PromiseIdentifier("tplus_actors_channel", "tplust_authen", "/endpoints/tplus/auth/appTicket")
@app.route(app_ticket_ep_promise.id, methods=["POST"])
# @PromisePool.deliver(app_ticket_ep_promise)
async def ep_tplus_auth_apptoken():
    __timber.info(app_ticket_ep_promise.id)
    __timber.info(request.data)

    app_ticket = AppTicketActor().resolve_ticket(request.json)

    promise = PromisePool.deliver(app_ticket_ep_promise)
    if promise is not None:
        promise.set_result(app_ticket)

    return AppTicketActor.success()



