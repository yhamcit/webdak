
from quart import Quart

from webapps.plugins.tplus.core import TplusPlugin
from webapps.modules.lumber.lumber import Lumber



_timber = Lumber.timber("root")
_err_timber = Lumber.timber("error")

_timber.info("Logging created. Prepare to launch.")
_timber.info("Creating webapps...")

app = Quart(__name__)

_timber.info("Webapp enter running status.")


# # health Check
@app.route("/endpoints/healthz")
async def hello():
    _timber.info("/endpoints/healthz")

    try:
        return TplusPlugin.success()
    except Exception as error:
        _err_timber.error(f"Caught exception: '{error}'.")
        return TplusPlugin.failure()


# tplus_endpoints_promise = PromiseIdentifier("tplus_endpoints_channel", "tplus_broker", "/endpoints/tplus/broker")
# @app.route(tplus_endpoints_promise.id, methods=["GET", "POST"])
# async def broker_tplus_endpoints():
#     _timber.info(tplus_endpoints_promise.id)

#     try:
#         return await None # 
#     except Exception as error:
#         _err_timber.error(f"Caught exception: '{error}'.")
#         return TplusPlugin.failure()


# cbs_endpoints_promise = PromiseIdentifier("cbs_endpoints_channel", "cbs_broker", "/endpoints/cbs/broker")
# @app.route(cbs_endpoints_promise.id, methods=["GET", "POST"])
# async def broker_cbs_endpoints():
#     _timber.info(cbs_endpoints_promise.id)

#     try:
#         return await None # 
#     except Exception as error:
#         _err_timber.error(f"Caught exception: '{error}'.")
#         return TplusPlugin.failure()



# app_tocken_actr_promise = PromiseIdentifier("tplus_actuators_channel", "tplus_authen", "/actuators/tplus/auth/appToken")
# @app.route(app_tocken_actr_promise.id, methods=["GET", "POST"])
# async def actor_tplus_app_token():
#     _timber.info(app_tocken_actr_promise.id)

#     try:
#         return await TplusPlugin().handle_msg(app_tocken_actr_promise, request)
#     except Exception as error:
#         _err_timber.error(f"Caught exception: '{error}'.")
#         return TplusPlugin.failure()


# tplus_authn_promise = PromiseIdentifier("tplus_actuators_channel", "tplus_authen", "/endpoints/tplus/push_msg")
# @app.route(tplus_authn_promise.id, methods=["POST"])
# async def endpoints_tplus_pushmsg():
#     _timber.info(f"Get endpoints_tplus_pushmsg via - {tplus_authn_promise.id}")

#     try:
#         return await TplusPlugin().handle_msg(tplus_authn_promise, request)
#     except Exception as error:
#         _err_timber.error(f"Caught exception: '{error}'.")
#         return TplusPlugin.success()




