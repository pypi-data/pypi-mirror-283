import json
from logging import LogRecord, Formatter

class LogFormatter(Formatter):
    
    def __init__(self) -> None:
        super().__init__()

    def format(self, record: LogRecord) -> str:

        log_data = {}
        log_data["_zl_timestamp"] = str(int(record.created)) + str(int(record.msecs))
        log_data["level"] = record.levelname
        log_data["message"] =  record.getMessage()

        return json.dumps(log_data)