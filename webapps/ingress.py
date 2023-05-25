from flask import Flask, request
from webapps.actors.tplus.auth.appticketactor import AppTicketActor
from webapps.model.properties.dao.actorenvironment import ActorsEnvironment

from webapps.model.properties.preference import Preference

from webapps.endpoints.tplus.auth.appticket import AppTicket
from webapps.modules.asyncoroutine.promisepool import PromisePool

from webapps.modules.lumber.lumber import Lumber


__timber = Lumber.timber("root")


app = Flask(__name__)



@app.route("/actors/tplus/auth/appToken", methods=["GET", "POST"])
async def actor_tplus_app_token():
    __timber.info("/actors/tplus/auth/appToken")

    if request.method == "POST":
        app_ticket = await AppTicketActor().renew_app_token()
    elif request.method == "GET":
        app_ticket = await AppTicketActor().exchange_app_token()
    else:
        return "rejected"
    
    return app_ticket


@app.route("/endpoints/healthz")
async def hello():
    __timber.info("/endpoints/tplus/auth/appToken")
    return "ok!"

@app.route("/endpoints/tplus/auth/appTicket", methods=["POST"])
async def ep_tplus_auth_apptoken():
    __timber.info("/endpoints/tplus/auth/appToken")

    __timber.info(request.json)

    promise = PromisePool().make_the_promise("actors_channel", "/endpoints/tplus/auth/appTicket", 
                                             "webapps.endpoints.tplus.auth.appticket.AppTicket")
    
    actor = AppTicketActor()
    result = actor.decrypt_push_message(request.json)
    token = AppTicket(result)

    promise.resovle(token)

    return AppTicketActor.success()


