
from asyncio import get_running_loop
import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import get_ident
from time import sleep
from quart import Quart

from webapps.plugins.tplus.core import TplusPlugin
from webapps.modules.lumber.lumber import Lumber

from multiprocessing import current_process


app = Quart(__name__)

# warning, these will also execute if this module imported
if not current_process().daemon:
    pass
else:
    print("Worker process running ... ")

    _timber = Lumber.timber("root")
    _err_timber = Lumber.timber("error")

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
