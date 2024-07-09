import os
from .utils import *
from . import logging
from .logging import logmanager

LOG_FORMAT = "[{time} / {severity}]{prefix} {message}"

def add(severity: str, message: str, prefix: str = '', color: str = WHITE) -> None:
    """
    Logs a custom message.

    Parameters
    -----------
    `severity` : :class:`str`, optional 
        The severity for the log message. Defaults to `''`.
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to `''`.
    `color` : :class:`str`, optional
        An optional color for the log message. Defaults to `WHITE`.
    """

    log(severity.upper(), message, prefix, color)

def info(message: str, prefix: str = '', color: str = BLUE) -> None:
    """
    Logs an informational message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to `''`.
    `color` : :class:`str`, optional
        An optional color for the log message. Defaults to `BLUE`.
    """
    log("INFO", message, prefix, color)

def debug(message: str, prefix: str = '', color: str = GREEN) -> None:
    """
    Logs a debug message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to `''`.
    `color` : :class:`str`, optional
        An optional color for the log message. Defaults to `GREEN`.
    """
    log("DEBUG", message, prefix, color)

def warn(message: str, prefix: str = '', color: str = YELLOW) -> None:
    """
    Logs a warning message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to `''`.
    `color` : :class:`str`, optional
        An optional color for the log message. Defaults to `YELLOW`.
    """
    log("WARN", message, prefix, color)

def error(message: str, prefix: str = '', color: str = RED) -> None:
    """
    Logs an error message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to `''`.
    `color` : :class:`str`, optional
        An optional color for the log message. Defaults to `RED`.
    """

    log("ERROR", message, prefix, color)

def critical(message: str, prefix: str = '', color: str = RED) -> None:
    """
    Logs a critical message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to `''`.
    `color` : :class:`str`, optional
        An optional color for the log message. Defaults to `RED`.
    """

    log("CRITICAL", message, prefix, color)

def log(severity: str, message: str, prefix: str, color: str = '') -> None:
    try:
        logger = logmanager.LoggerManager.get_logger()  # Get the configured logger
    except Exception as e:
        logger = None   

    log_format = os.getenv("CLI-LOG_FORMAT", LOG_FORMAT)
    time = format_time()
    lines = message.split('\n') # Split the message into lines
    lines = [log_format.format(prefix=(f"[{prefix}]" if prefix else ""), severity=severity, message=line, time=time) for line in lines if line.strip()] # Prepend each line with the timestamp and severity information
    msg_console = '\n'.join(lines) # Join the lines back together
    log_to_console(msg_console, color)

    for line in message.split('\n'):
        if line.strip():  # Skip empty lines
            if logger:
                if severity == "INFO":
                    logger.info(line)
                elif severity == "DEBUG":
                    logger.debug(line)
                elif severity == "WARN":
                    logger.warning(line)
                elif severity == "ERROR":
                    logger.error(line)
                elif severity == "CRITICAL":
                    logger.critical(line)
                else:
                    logger.log(logging.INFO, line)

def log_to_console(message: str, color: str = ''):
    print(color + message)