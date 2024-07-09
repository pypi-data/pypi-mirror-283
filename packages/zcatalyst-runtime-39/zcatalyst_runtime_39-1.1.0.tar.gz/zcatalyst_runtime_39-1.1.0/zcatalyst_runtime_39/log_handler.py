import os
import logging

from init_handler import InitHandler
from log_formatter import LogFormatter

class LogHandler(logging.Handler):
    SPARKP_LOG_PATH = 0
    SPARKP_ADD_LOG_APPEND_PATH = 1
    SPARKP_REMOVE_LOG_APPEND_PATH = 2

    def __init__(self) -> None:
        super().__init__()
        
        if InitHandler.is_local():
            self.setFormatter(logging.Formatter(fmt='%(created)d%(msecs)d\t%(levelname)s\t%(message)s\n'))
            return None
        
        self.setFormatter(LogFormatter())

        log_fd = int(os.getenv('X_ZOHO_SPARKLET_LOG_FD'))
        del os.environ['X_ZOHO_SPARKLET_LOG_FD']
        pid = os.getpid()

        self.log_fd = open(f'/proc/{pid}/fd/{log_fd}', 'wb', buffering=0)

    def send_sparkp_log(self, path: int, message: str) -> None:
        # Handovers logs of the function to runtime provided LOG_FD.
        # 
        #    +-------------------+---------------+----------------------+----------------------------+
        #    | ENCODING (1 byte) | PATH (1 byte) | CONTENT_LEN (4 byte) | MESSAGE (CONTENT_LEN byte) |
        #    +-------------------+---------------+----------------------+----------------------------+
        # 
        # First 1 byte is the encoding, for logs it is always 2.
        # Second 1 byte is the path, for logs it can be -
        #       0 to send log message,
        #       1 to add to log_appends, 
        #       2 to remove from log_appends.
        # Third 4 bytes are the content length, For logs it will be length of the message. (big-endian)
        # Next CONTENT_LEN byte is the message. (utf-8)
        formatted_log = bytearray()

        formatted_log[0:1] = (2).to_bytes(1, 'big')
        formatted_log[1:2] = (path).to_bytes(1, 'big')
        formatted_log[2:6] = len(message).to_bytes(4, 'big')
        formatted_log[6:] = message.encode('utf-8')

        self.log_fd.write(formatted_log)

   
    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)

        if InitHandler.is_local():
            print(message)
            return None

        self.send_sparkp_log(self.SPARKP_LOG_PATH, message)
