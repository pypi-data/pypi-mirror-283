# Command Line Interface Log

This python module is used to make your command line / terminal more fancy when printing / logging certain events.

For a more detailed documentation checkout the docs: https://deltabotics.github.io/cli-log

## Quick install

```bash
pip install cli-log
```

## Examples

### Basic usage
```python
import cli

cli.info("Hello world!\nInfo event.")
cli.debug("Debug event.")
cli.warn(prefix="CORE", message="Warning event.")
cli.error("Error event.")
```

```log
[16:30:52 / INFO] Hello world!
[16:30:52 / INFO] Info event.
[16:30:52 / DEBUG] Debug event.
[16:30:52 / WARN][CORE] Warning event.
[16:30:52 / ERROR] Error event.
```

### Advanced usage
```python
import cli

cli.info("Hello world!")
cli.add(severity="Testing", message="Hello", prefix="test", color=cli.MAGENTA)
cli.init(log_format="[{time} ! {severity}]{prefix} {message}", reset=True)
cli.error("Error between error raising.")
cli.init(reset=True) # Doesn't do anything because we didnt set format before
cli.debug("Should not get executed.")
cli.init(log_format="[{severity} ! {time}]{prefix} {message}")
cli.info(message="Hello", color=cli.BLACK)
```

```log
[16:30:52 / INFO] Hello world!
[16:30:52 / TESTING][test] Hello
Traceback (most recent call last):
    File "usr/local/lib/python3.11/site-packages\cli-log\initialise.py", line 18, in init
        raise ValueError("Cannot use 'reset' parameter in combination with 'log_format'")
ValueError: Cannot use 'reset' parameter in combination with 'log_format'

[16:30:52 ! ERROR] Error between error raising.
[16:30:52 / DEBUG] Should not get executed.
[16:30:52 ! INFO] Hello
```
Here you can see that an error was raised due to the usage of the `reset` parameter in combination with the `log_format` parameter.

You can also see that the `[16:30:52 / DEBUG]` is not using `[16:30:52 ! DEBUG]` because the format was reset.
