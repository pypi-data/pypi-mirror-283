#!/usr/bin/env python

import logging


def subscribe_to_logger():
    """
    Subscribes module to general logger

    Returns:
        logger - Logger object for that module
    """
    logger = logging.getLogger(__name__)
    return logger


def configure_logger(debug=bool(False)):
    """
    Initializes a logger handler to log events

    Arguments:
        debug - Enable debug mode during invocation

    Returns:
        logger - Logger handler
    """
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    formatter = logging.Formatter(fmt="%(levelname)s\t(%(module)s)\t%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = subscribe_to_logger()
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger
