import logging
from flask import request, url_for
from cowork_site import config


def configure_logger(logger, log_level):
    formatter = logging.Formatter(
        '[%(asctime)s] - %(module)s - %(levelname)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger


def back_redirect_url(default='postings.posting_list'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def is_admin(user):
    return config.Configuration.ADMIN_EMAIL and user.email == config.Configuration.ADMIN_EMAIL