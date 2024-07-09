import os
import multiprocessing
from pathlib import Path

class InitHandler:
    init_status = multiprocessing.Event()
    if os.getenv('X_ZOHO_CATALYST_FUNCTION_LOADED') == 'true':
        init_status.set()

    __listen_host = os.getenv('X_ZOHO_CATALYST_LISTEN_HOST', '0.0.0.0')
    __listen_port = os.getenv('X_ZOHO_CATALYST_SERVER_LISTEN_PORT', os.getenv('X_ZOHO_SPARKLET_SERVER_LISTEN_PORT', 9000))
    __is_local = os.getenv('X_ZOHO_CATALYST_IS_LOCAL') == 'true'
    __code_location = Path(os.getenv('X_ZOHO_CATALYST_CODE_LOCATION', '/catalyst'))

    def get_worker_count():
        return 4
    
    def get_thread_count():
        return 4

    def get_listen_host() -> int:
        return InitHandler.__listen_host
    
    def get_listen_port() -> int:
        return InitHandler.__listen_port
    
    def is_local() -> bool:
        return InitHandler.__is_local

    def get_code_location() -> Path:
        return InitHandler.__code_location
    
    def is_success():
        InitHandler.init_status.is_set()
    
    def mark_success():
        InitHandler.init_status.set()

    def wait():
        InitHandler.init_status.wait()

    def update_status():
        if InitHandler.is_local():
            return

        # Updates the status of the function to runtime.
        # 
        #    +---------------------+-----------------+------------------------+-------------------+
        #    |  ENCODING (1 byte)  |  PATH (1 byte)  |  CONTENT_LEN (4 byte)  |  STATUS (1 byte)  |
        #    +---------------------+-----------------+------------------------+-------------------+
        # 
        # First 1 byte is the encoding, for status it is always 1.
        # Second 1 byte is the path, for status it is always 0.
        # Third 4 bytes are the content length. For status(unsigned-8bit) this will always be 1. (big-endian)
        # Next 1 byte is status.

        status_frame = bytearray()
        status_frame[0:1] = (1).to_bytes(1, 'big')
        status_frame[1:2] = (0).to_bytes(1, 'big')
        status_frame[2:6] = (1).to_bytes(4, 'big')
        status_frame[6:7] = (1).to_bytes(1, 'big')

        status_fd = int(os.getenv('X_ZOHO_SPARKLET_STATUS_FD'))
        del os.environ['X_ZOHO_SPARKLET_STATUS_FD']

        pid = os.getpid()
        status_fd = open(f'/proc/{pid}/fd/{status_fd}', 'wb', buffering=0)

        status_fd.write(status_frame)
