import logging
from functools import lru_cache


@lru_cache(maxsize=None)
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
