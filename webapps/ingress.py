import encodings
import mimetypes
from os import path
from quart import Quart, abort, request, send_from_directory
from quart_cors import cors

from webapps.plugins.tplus.core import TplusPlugin
from webapps.modules.lumber.lumber import Lumber

from multiprocessing import current_process



app = Quart(__name__, static_folder=None)
app = cors(app, allow_origin=["https://web.cdyhamc.com", "https://web.cdyhamc.com:9051"], allow_headers=["content-type"], allow_methods=["POST", "GET", "OPTIONS"])

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

    # 支持的压缩类型及其文件扩展名
    COMPRESSION_TYPES = {'br': '.br', 'gzip': '.gz'}

    @app.route('/static/<path:filename>')
    async def serve_static(filename):
        static_dir = "/home/harvey/studio/webdak/webapps/static"
        file_path = path.join(static_dir, filename)
        
        # 检查原始文件是否存在
        if not path.isfile(file_path):
            abort(404)

        # 获取客户端支持的压缩类型
        accept_encoding = request.headers.get('Accept-Encoding', '').lower()
        
        # 遍历支持的压缩类型，检查是否存在预压缩文件
        if not 'gzip' in set(accept_encoding.split(',')):
            abort(404)

        response = await send_from_directory(
            static_dir, filename,
            mimetype='application/json'
        )
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Vary'] = 'Accept-Encoding'
        return response
