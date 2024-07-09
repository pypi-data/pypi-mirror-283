import os, traceback

def init(log_format = None, reset: bool = False) -> None:
    """
    Initializes the cli-log with a custom log format.

    Parameters
    -----------
    `log_format` : :class:`str`, optional
        Custom log format. Defaults to `[{time} / {severity}]{prefix} {message}`.
    `reset` : :class:`bool`, optional
        Resets the `log_format` to it's default value when set to `True`. Defaults to `False`.
        NOTE: This parameter cannot be used in combination with `log_format`.
    """

    try:
        if log_format and reset == True:
            raise ValueError("Cannot use 'reset' parameter in combination with 'log_format'")
        elif log_format:
            os.environ["CLI-LOG_FORMAT"] = log_format
        elif reset == True:
            del os.environ["CLI-LOG_FORMAT"]
    except KeyError as e:
        if 'CLI-LOG_FORMAT' in str(e):
            pass # This error can be ignored safely.
    except Exception:
        print(traceback.format_exc())