import logging

log_format = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)
log_handler = logging.FileHandler("./log/app.log")
log_handler.setFormatter(log_format)

logger = logging.getLogger("calculator")
logger.addHandler(log_handler)