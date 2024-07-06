# -*- coding: utf-8 -*-

from loguru import logger
from .paths import path_root_log


def get_logger():
    logger.remove()
    logger.add(
        str(path_root_log),
        format="{time: YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
        rotation="1 MB",
    )
    return logger
