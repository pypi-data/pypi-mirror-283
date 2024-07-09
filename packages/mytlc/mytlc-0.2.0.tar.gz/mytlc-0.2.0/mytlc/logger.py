# logger.py
# Global logging system configuration module for the mytlc module.
# Defines a standard configuration that can be imported and used in all parts of the module.

import logging

from .constants import LOG_FILENAME


def configure_logging() -> None:
    """Configures the global logging for the module.

    This function configures logging to write messages both to the console and to a log file.
    The format of log messages includes time, severity level, and message.

    Example of use:
        configure_logging()
        logging.info("Test log message")
    """

    # Mandatory to be able to log correctly in all levels
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Definition of log format
    custom_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=custom_format)

    # Configuration to write to a file (in addition to the console)
    file_handler = logging.FileHandler(LOG_FILENAME)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(custom_format))

    logging.getLogger("").addHandler(file_handler)
