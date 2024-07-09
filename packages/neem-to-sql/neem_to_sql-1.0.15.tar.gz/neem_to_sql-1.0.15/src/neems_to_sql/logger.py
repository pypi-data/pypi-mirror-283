import logging
import os

from typing_extensions import Optional


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    info_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + info_format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomLogger:
    """
    A custom logger class that can be used to log messages to the console and to a file at the same time.
    This class is a singleton class, meaning that only one instance of this class can be created.
    """
    LOGGER: Optional[logging.Logger] = None
    """The logger object that is used to log messages to the console"""
    FILE_HANDLER: Optional[logging.FileHandler] = None
    """The file handler object that is used to log messages to a file."""
    LOG_FILE: Optional[str] = None
    """The name of the log file"""
    def __init__(self, name: Optional[str] = "NEEM_SQLIZER",
                 log_file: Optional[str] = "stdout_file.txt",
                 log_level: Optional[int] = logging.INFO,
                 reset_handlers: Optional[bool] = False):
        if CustomLogger.LOGGER is not None:
            if reset_handlers:
                # remove the existing logger
                CustomLogger.LOGGER.removeHandler(CustomLogger.FILE_HANDLER)
                # remove created file
                os.system(f"rm {CustomLogger.LOG_FILE}")
            else:
                return
        CustomLogger.LOGGER = self._init_logger(name, log_level)
        CustomLogger.LOGGER.setLevel(log_level)
        CustomLogger.LOG_FILE = log_file
        CustomLogger.FILE_HANDLER = self._init_log_file_handler()

    @staticmethod
    def _init_logger(name: str, log_level: int) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        return logger

    @classmethod
    def _init_stream_handler(cls, log_file: str, log_level: int) -> logging.StreamHandler:
        stream_handler = logging.StreamHandler(open(log_file, "w"))
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(CustomFormatter())
        cls.LOGGER.addHandler(cls.stream_handler)
        return stream_handler

    @classmethod
    def get_logger(cls):
        return cls.LOGGER

    @classmethod
    def get_log_level(cls):
        return cls.LOGGER.getEffectiveLevel()

    @classmethod
    def get_log_level_name(cls):
        return logging.getLevelName(cls.LOGGER.getEffectiveLevel())

    @classmethod
    def set_logger_name(cls, name):
        cls.LOGGER.name = name

    @classmethod
    def _init_log_file_handler(cls, clear_file=True):
        if clear_file:
            # clear the log file
            open(cls.LOG_FILE, "w").close()
        file_handler = logging.FileHandler(cls.LOG_FILE)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(CustomFormatter())
        cls.LOGGER.addHandler(file_handler)
        return file_handler

    @classmethod
    def set_log_level(cls, level):
        cls.LOGGER.setLevel(level)
        cls.FILE_HANDLER.setLevel(level)
