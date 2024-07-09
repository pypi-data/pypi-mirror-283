"""
# Logging

Built in logging functionality.
"""

from .levels import DEBUG, INFO, WARNING, ERROR, CRITICAL
from .initialise import init
from .FileHandler import OverwriteFileHandler as FileHandler
from logging.handlers import SysLogHandler

__all__ = ["init", "FileHandler", "SysLogHandler"] # More to be added.