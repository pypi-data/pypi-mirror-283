import os
import sys
import time
import zipfile
import json
import logging
import signal

from flask import Flask, request, Response, g, current_app

from log_handler import LogHandler
from init_handler import InitHandler
from signal_handler import sigterm_handler
from flavours import FlavourHandler
from flavours.utils import set_response_json

ZIP_LOCATION: str = '/tmp/code.zip'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handler = LogHandler()
logger.addHandler(log_handler)

# To support user function to import their own modules and prefer
# locally installed modules over globally installed modules.
sys.path.insert(0, InitHandler.get_code_location().as_posix())

app = Flask(__name__)

def internal_request_handler():
    if request.path == '/init':
        if InitHandler.is_success():         
            # Will be caught by uncaught exception handler
            raise Exception('init already completed')
        
        init_start_time = int(time.time() * 1000)

        with open(ZIP_LOCATION, 'wb') as code_zip:
            while True:
                chunk = request.stream.read(1048576)

                if not chunk:
                    break
                code_zip.write(chunk)
                
        with zipfile.ZipFile(ZIP_LOCATION, 'r') as code_zip:
            code_zip.extractall(InitHandler.get_code_location())
            os.remove(ZIP_LOCATION)

        InitHandler.mark_success() 

        g.response.headers.add('x-catalyst-init-time-ms', f'{int(time.time() * 1000)} - {init_start_time}')
        set_response_json(200, { 'message': 'success' })
    elif request.path == '/ruok':
        set_response_json(200, { 'message': 'iamok' })
    else:
        raise Exception('unexpected internal path')

FLAVOUR_HANDLER: FlavourHandler = FlavourHandler() if InitHandler.is_success() else None

def customer_request_handler():
    logger.info(f'Execution started at: {int(time.time() * 1000)}')

    global FLAVOUR_HANDLER
    if not FLAVOUR_HANDLER:
        FLAVOUR_HANDLER = FlavourHandler()
            
    try:
        FLAVOUR_HANDLER.invoke_handler()
    except Exception as e:
        logger.exception(repr(e))
        FLAVOUR_HANDLER.return_error_response(repr(e))

@app.route('/', methods=['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/<path:_path>', methods=['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def router(_path = None):
    g.response = Response()

    if request.headers.get('x-zoho-catalyst-internal') == 'true':        
        internal_request_handler()
    else:
        InitHandler.wait()

        if request.headers.get('x-zc-request-uuid') is not None:
            log_handler.send_sparkp_log(log_handler.SPARKP_ADD_LOG_APPEND_PATH, message= json.dumps({"request_uuid": request.headers.get('x-zc-request-uuid')}))
        customer_request_handler()
    return g.response

@app.errorhandler(Exception)
def error_handler(e):
    # We caught all customer request exceptions in `customer_request_handler` 
    # itself, so we're marking this exception as an internal failure.  
    with app.app_context():
        setattr(current_app, '__internal_failure', True)
    logger.exception(repr(e))
    set_response_json(500, { 'error': repr(e) })
    return g.response

def run_production_server():
    from gunicorn.app.base import BaseApplication

    # Gunicorn custom application
    # Refer: https://docs.gunicorn.org/en/stable/custom.html
    class CatalystApplication(BaseApplication):
        def __init__(self, app, options = {}):
            self.app = app
            self.options = options

            super().__init__()

        def init(self, parser, opts, args):
            return super().init(parser, opts, args)

        def load(self):
            return self.app
        
        def load_config(self):
            for k, v in self.options.items():
                if k not in self.cfg.settings:
                    print('invalid: ', k)
                    continue

                try:
                    self.cfg.set(k.lower(), v)
                except Exception:
                    raise Exception(f'Invalid value for: {k}: {v}')
                
    # Gunicorn server hooks
    # Refer: https://docs.gunicorn.org/en/stable/settings.html#server-hooks

    # Hook: when_ready
    def when_ready(_server):
        """Called just after the server is started."""

        if InitHandler.is_local():
            return

        InitHandler.update_status()

    # Hook: post_request
    def post_request(_worker, _req, _environ, _resp):
        """Called after a worker processes the request."""

        # Since, `error_handler`` marked this as an internal failure, we're sending
        # the SIGINT signal to master process.
        with app.app_context():
            if getattr(current_app, '__internal_failure', False):
                os.killpg(os.getppid(), signal.SIGINT)

    # Hook: child_exit
    def child_exit(_server, _worker):
        """Called just after a worker has been exited, in the master process."""

        os._exit(signal.SIGUSR1)

    options = {
        'bind': f'{InitHandler.get_listen_host()}:{InitHandler.get_listen_port()}',
        'workers': InitHandler.get_worker_count(),
        'threads': InitHandler.get_thread_count(),
        'pythonpath': f'{InitHandler.get_code_location()},',
        'preload_app': True,
        'loglevel': 'warning',
        'timeout': 0,
        'graceful_timeout': 5,
        # Server hooks
        'when_ready': when_ready,
        'child_exit': child_exit,
        'post_request': post_request,
    }

    CatalystApplication(app, options).run()

def run_development_server():
    # Note:
    # The reason for adding SIGTERM signal handler only in development server is 
    # it is already handled in Gunicorn side for production server.
    signal.signal(signal.SIGTERM, sigterm_handler)

    # To disable Flask's server banner and console logs
    from flask import cli
    cli.show_server_banner = lambda *args: None
    logging.getLogger('werkzeug').disabled = True
    app.run('0.0.0.0', InitHandler.get_listen_port())

if __name__ == "__main__":
    try:
        if os.getenv('CATALYST_FUNCTION_TYPE') == 'job':
            InitHandler.update_status()
            customer_request_handler()
        else:
            if not InitHandler.is_local():
                run_production_server()
            else:
                run_development_server()
    except Exception as e:
        logger.exception(e)
        os._exit(signal.SIGUSR1)