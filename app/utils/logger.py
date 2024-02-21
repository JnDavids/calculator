import logging
from logging import Logger


def get_logger(name: str) -> Logger:
    log_format = logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    log_handler = logging.FileHandler("./log/app.log")
    logger = logging.getLogger(name)

    log_handler.setFormatter(log_format)
    logger.addHandler(log_handler)

    return logger