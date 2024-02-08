import os

from loguru import logger
from . import config


def toggle_activation():
    config.IS_ACTIVE = not config.IS_ACTIVE
    if config.IS_ACTIVE:
        logger.info("Program re-activated")
    else:
        logger.info("Program suspended")


def launch(param):
    if config.IS_ACTIVE:
        logger.info(f"launch {param}")
        os.system(param)
