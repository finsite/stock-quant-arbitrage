import logging
import os


def setup_logger(name: str = "app") -> logging.Logger:
    """Sets up and returns a logger with the specified name.

    If a logger with the same name already exists, it is reused.
    Otherwise, a new logger is created and configured to log to stdout
    with the format:
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    The log level and format are controlled via environment variables:
        - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
        - LOG_FORMAT: "json" for structured logging, anything else for plain text

    Args:
    ----
        name (str): The name of the logger. Defaults to "app".

    Returns:
    -------
        logging.Logger: Configured logger instance.
    """
    logger: logging.Logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        log_format = os.getenv("LOG_FORMAT", "plain").lower()

        if log_format == "json":
            formatter = logging.Formatter(
                '{"timestamp":"%(asctime)s","name":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
            )
        else:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

    return logger
