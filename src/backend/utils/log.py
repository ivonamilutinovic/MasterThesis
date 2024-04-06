import logging
import os
import sys
from contextlib import suppress
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from logging import Logger


def get_logger(module_name: str) -> 'Logger':
    logger = logging.getLogger(module_name)
    return logger


def setup_logger(logfile: Optional[str] = None, console_threshold: int = logging.WARNING,
                 logfile_threshold: int = logging.WARNING, brief_console_format: bool = False,
                 force_colors: bool = False):
    """ Setup backend library logger. """

    verbose_format = '%(asctime)-15s %(levelname)-8s %(name)s: %(message)s'
    brief_format = '[%(levelname)s] %(name)s: %(message)s'

    log_handlers = []

    console_formatter = ColoredLogFormatter(brief_format if brief_console_format else verbose_format,
                                            force_colors=force_colors)
    console_log = logging.StreamHandler(sys.stdout)
    console_log.setFormatter(console_formatter)
    console_log.setLevel(console_threshold)
    log_handlers.append(console_log)

    if logfile:
        file_formatter = logging.Formatter(verbose_format)
        logfile = logfile if logfile.endswith(".log") else f"{logfile}.log"
        create_subfolders_to(logfile)
        file_log = logging.FileHandler(logfile, mode='w')
        file_log.setFormatter(file_formatter)
        file_log.setLevel(logfile_threshold)
        log_handlers.append(file_log)

    library_logger = logging.getLogger("backend")
    library_logger.setLevel(logging.DEBUG)

    for handler in list(library_logger.handlers):
        library_logger.removeHandler(handler)

    for handler in log_handlers:
        library_logger.addHandler(handler)


class ColoredLogFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        force_colors = kwargs.pop("force_colors", False)
        if self._stdout_supports_ansi() or force_colors:
            self._IMPORTANT_START = "\033[36;1m"  # cyan, bold
            self._WARNING_START = "\033[93;1m"    # bright yellow, bold
            self._ERROR_START = "\033[91;1m"      # bright red, bright/bold
            self._END = "\033[0m"                 # reset all attributes
        else:
            self._IMPORTANT_START = ''
            self._WARNING_START = ''
            self._ERROR_START = ''
            self._END = ''
        super().__init__(*args, **kwargs)

    @staticmethod
    def _stdout_supports_ansi():
        if 'PYCHARM_HOSTED' in os.environ:
            # PyCharm Console supports ANSI colors

            # Don't use colored output when running tests
            # -> PyCharm XML parser has a bug and cannot reload test result xml files with color codes in it...
            pytest_hosted = "pytest" in sys.modules
            return not pytest_hosted
        if ('ANSICON' in os.environ) or ('ANSI' in os.environ.get('TERM', "")):
            return True  # Console claims ANSI support
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty() and os.name != 'nt':
            return True  # Non-Windows console, most probably has ANSI support

        return False  # Neiter ANSI Term nor Unix TTY

    def format(self, record: logging.LogRecord):
        formatted_message = super().format(record)
        if record.levelno == logging.INFO and getattr(record, "important", False):
            formatted_message = self._IMPORTANT_START + formatted_message + self._END
        elif record.levelno == logging.WARNING:
            formatted_message = self._WARNING_START + formatted_message + self._END
        elif record.levelno == logging.ERROR:
            formatted_message = self._ERROR_START + formatted_message + self._END
        return formatted_message


def create_subfolders_to(filename: str):
    """
        Creating (sub)folders to provided filename (path) argument.

        Check if filename argument has actual file name in itself (if filename has any extension in itself, then passed
        filename argument has actual file name in itself) ---> create all folders that are above that actual file
        name in provided path.
        Otherwise, filename argument is actually (sub)folders structure that needs to be created if it doesn't exist.
    """

    with suppress(FileNotFoundError):
        if not os.path.splitext(filename)[1]:
            os.makedirs(os.path.normpath(filename), exist_ok=True)
        else:
            os.makedirs(os.path.dirname(os.path.normpath(filename)), exist_ok=True)
