import logging as real_logging # Real logging package
from . import levels as logging # Custom logging package
from .FileHandler import OverwriteFileHandler
from logging.handlers import SysLogHandler
from logging import StreamHandler

logger = None

class LoggerManager:
    _logger = None

    @staticmethod
    def init(
            level = logging.DEBUG, handler_type = 'syslog', facility = SysLogHandler.LOG_DAEMON, address = '/dev/log', log_file_path = None,
            mode = 'a', max_bytes = 10485760, backup_count = 5, stream = None, fmt="%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - '%(message)s'",
            datefmt="%Y-%m-%d %H:%M:%S"
        ) -> None:

        logger = real_logging.getLogger(__name__)
        logger.setLevel(level)

        if handler_type == 'syslog':
            if not hasattr(real_logging, 'SysLogHandler'):
                raise ValueError("Syslog logging is not supported on this platform.")
            handler = SysLogHandler(facility=facility, address=address)
        elif handler_type == 'file':
            if log_file_path is None:
                raise ValueError("log_file_path must be specified for file handler")
            elif mode is not None and mode not in ('a', 'w'):
                raise ValueError("mode must be one of 'a' (append), 'w' (write)")
            handler = OverwriteFileHandler(log_file_path, mode=mode, maxBytes=max_bytes, backupCount=backup_count)
        elif handler_type == 'stream':
            handler = StreamHandler(stream=stream)
        else:
            raise ValueError("Invalid handler_type specified. Choose 'syslog', 'file', or 'stream'.")

        formatter = real_logging.Formatter(fmt=fmt, datefmt=datefmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        LoggerManager._logger = logger
    
    @staticmethod
    def get_logger():
        if LoggerManager._logger is None:
            raise RuntimeError("Logger is not initialized. Call 'init' first.")
        return LoggerManager._logger