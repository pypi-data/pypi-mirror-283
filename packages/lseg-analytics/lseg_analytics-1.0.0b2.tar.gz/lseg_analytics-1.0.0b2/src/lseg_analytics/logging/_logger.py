import functools
import inspect
import logging
import sys
from logging import Formatter, Logger, StreamHandler
from logging.handlers import RotatingFileHandler

from ._config import LoggingOutput, library_config

# Disable logId for HTTP trace since it has no such ID
# _FORMAT = "[%(levelname)s]\t[%(asctime)s]\t[%(threadName)s]\t[%(name)s]\t[%(filename)s:%(lineno)d]\t[Log ID: %(logId)d] %(message)s"
_FORMAT = "[%(levelname)s]\t[%(asctime)s]\t[%(threadName)s]\t[%(name)s]\t[%(filename)s:%(lineno)d]\t %(message)s"

_formatter = Formatter(fmt=_FORMAT)

_global_file_handler = RotatingFileHandler(
    filename="lseg_analytics.log", maxBytes=10 * 1024 * 1024, encoding="utf-8", mode="w"
)
_global_file_handler.setFormatter(_formatter)


def get_library_logger(name: str) -> "LibraryLogger":
    logging.setLoggerClass(LibraryLogger)
    logger = LibraryLoggerAdapter(logging.getLogger(name))  # type: ignore
    logging.setLoggerClass(Logger)
    return logger  # type: ignore


class LibraryLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger: "LibraryLogger"):
        super().__init__(logger, {})
        self.logging_transaction_requests_counter = 0
        self.current_log_id = 0

    def __enter__(self):
        self.logging_transaction_requests_counter += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logging_transaction_requests_counter -= 1
        if self.logging_transaction_requests_counter == 0:
            self.current_log_id += 1

    def process(self, msg, kwargs):
        log_id = self.current_log_id
        if self.logging_transaction_requests_counter == 0:
            self.current_log_id += 1
        kwargs["extra"] = {"logId": log_id}
        return msg, kwargs

    def hold_log_id(self, f):
        if inspect.isgeneratorfunction(f):
            self.warning("TODO: Using wrapper doesn't work with generators properly (wrapper called twice)")

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return wrapper


class LibraryLogger(Logger):
    def __init__(self, name: str):
        super().__init__(name=name)
        self._subscribe_logger_to_config()
        self.update_config()

    def update_config(self):
        self.handlers.clear()
        for output in self._config.outputs:
            if output == LoggingOutput.STDOUT:
                self._add_stdout_handler()
            elif output == LoggingOutput.FILE:
                self._add_file_handler()
        self.update_level_from_config()

    def update_level_from_config(self):
        self.setLevel(self._config.level)

    def _subscribe_logger_to_config(self):
        self._config.add_logger(self)
        library_config["DEFAULT"].add_logger(self)

    def _add_stdout_handler(self):
        handler = StreamHandler(stream=sys.stdout)
        handler.setFormatter(_formatter)
        self.addHandler(handler)

    def _add_file_handler(self):
        self.addHandler(_global_file_handler)

    @property
    def _config(self):
        return library_config[self.name]


# For HTTP trace debugging log
http_logger = get_library_logger("corehttp")
