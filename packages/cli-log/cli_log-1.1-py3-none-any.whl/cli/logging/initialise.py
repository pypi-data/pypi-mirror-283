import os
from . import levels as logging
from .logmanager import LoggerManager
from logging.handlers import SysLogHandler

def init(
        level = logging.DEBUG,
        handler_type = 'syslog',
        facility = SysLogHandler.LOG_DAEMON,
        address = os.path.join('dev', 'log'),
        log_file_path = None,
        mode = 'a',
        max_bytes = 10485760,
        backup_count = 5,
        stream = None,
        fmt = "%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - '%(message)s'",
        datefmt = "%Y-%m-%d %H:%M:%S"
        ) -> None:

        """
        Initialises the logging system with the specified options.

        Parameters
        ----------
        `level` : :class:`int`, optional
            The logging level (e.g., `logging.DEBUG`, `logging.INFO`). Defaults to `logging.DEBUG`.
        `handler_type` : :class:`str`, optional	
            Type of logging handler (`'syslog'`, `'file'`, `'stream'`). Defaults to `'syslog'`.
        `facility` : :class:`int`, optional
            Syslog `facility` if `handler_type` is `'syslog'`. Defaults to `SysLogHandler.LOG_DAEMON`.
        `address` : :class:`str`, optional
            Address for syslog logging if `handler_type` is 'syslog'. Defaults to `'/dev/log'`.
        `log_file_path` : :class:`str`, optional
            Path to the log file if `handler_type` is `'file'`. Required if `handler_type` is `'file'`.
        `mode` : :class:`str`, optional
            Mode for opening the log file if `handler_type` is `'file'`. Defaults to `'a'` (append mode).
        `max_bytes` : :class:`int`, optional
            Maximum size of the log file before rotation (used with `'file'` handler). Defaults to `10485760` bytes (10 MB).
        `backup_count` : :class:`int`, optional
            Number of backup log files to keep (used with `'file'` handler). Defaults to `5`.
        `stream` : :class:`file-like object`, optional
            Stream to log to if `handler_type` is `'stream'` (e.g., `sys.stdout`). Defaults to `None`.
        `fmt` : :class:`str`, optional
            Log message format. Defaults to `"%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - '%(message)s'"`.
        `datefmt` : :class:`str`, optional
            Date/time format for log messages. Defaults to `"%Y-%m-%d %H:%M:%S"`.
        """

        LoggerManager.init(
                level=level,
                handler_type=handler_type,
                facility=facility,
                address=address,
                log_file_path=log_file_path,
                mode=mode, max_bytes=max_bytes,
                backup_count=backup_count,
                stream=stream,
                fmt=fmt,
                datefmt=datefmt
                )