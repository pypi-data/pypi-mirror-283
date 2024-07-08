# encoding:utf-8
import logging

class LogLevel:

    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10


class _MyLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)
        log_formatter = logging.Formatter('%(name)s|%(levelname)s|%(filename)s|%(lineno)d|%(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.addHandler(console_handler)


log_ld = _MyLogger("零动插件", logging.ERROR)
log = _MyLogger("日志", logging.DEBUG)

__all__ = ['log_ld', 'log', "LogLevel"]
