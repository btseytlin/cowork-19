import logging


def configure_logger(logger, log_level):
    formatter = logging.Formatter(
        '[%(asctime)s] - %(module)s - %(levelname)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger
