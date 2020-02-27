from enum import Enum


class LogType(Enum):
    DEBUG = 0,
    Warning = 1,
    Error = 2


class Log:
    def __init__(self, message: str, log_type: LogType = LogType.DEBUG, timestamp=0):
        self.message = message
        self.log_type = log_type
        self.timestamp = timestamp
