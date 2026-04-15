import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

#  format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

#  console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

#  file handler
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

#  attach handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)