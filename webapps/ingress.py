
from quart import Quart, request

from webapps.actuators.tplus.auth.appticketactor import AppTicketActor
from webapps.language.errors.tpluserror import AppTicketExpired, AppTicketNotAvialable
from webapps.model.properties.dao.actorenvironment import actuatorsEnvironment

from webapps.model.properties.preference import Preference

from webapps.endpoints.tplus.auth.appticket import AppTicket
from webapps.modules.coroutinpromise.promisepool import PromisePool
from webapps.modules.coroutinpromise.promisepool import PromiseIdentifier

from webapps.modules.lumber.lumber import Lumber



app = Quart(__name__)

__timber = Lumber.timber("root")

__timber.info("Webapp enter running status.")


app_tocken_actr_promise = PromiseIdentifier("tplus_actuators_channel", "tplus_authen", "/actuators/tplus/auth/appToken")
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
    __timber.info("AppTicketActor.renew_app_token()")

    app_ticket = await PromisePool.for_promise(app_tocken_actr_promise, None)
    app_token = await AppTicketActor().exchange_app_ticket(app_ticket)
    
    return app_token


@app.route("/endpoints/healthz")
async def hello():
    __timber.info("/endpoints/healthz")
    return AppTicketActor.success()


app_ticket_ep_promise = PromiseIdentifier("tplus_actuators_channel", "tplus_authen", "/endpoints/tplus/auth/appTicket")
@app.route(app_ticket_ep_promise.id, methods=["POST"])
# @PromisePool.deliver(app_ticket_ep_promise)
async def ep_tplus_auth_apptoken():
    __timber.info(app_ticket_ep_promise.id)

    content = await request.get_json()
    __timber.info(content)

    app_ticket = AppTicketActor().resolve_ticket(content)

    PromisePool.deliver(app_ticket_ep_promise, app_ticket)

    return AppTicketActor.success()

