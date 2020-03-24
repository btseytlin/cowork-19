from flask import Flask, abort
from flask.logging import default_handler
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException

from cowork_site import config
from cowork_site.utils import configure_logger
from cowork_site.db import configure_database

from cowork_site.candidates.blueprint import candidates_blueprint


def configure_app(app, config):
    app.config.from_object(config)


def configure_logging(app, log_level):
    app.logger.removeHandler(default_handler)
    configure_logger(app.logger, log_level)


def create_app(config=config.Configuration, session_factory=None):
    app = Flask(__name__)
    CORS(app)
    configure_logging(app, config.LOG_LEVEL)
    configure_app(app, config)
    configure_database(app, config.SQLALCHEMY_URL, config.DB_ECHO, session_factory)

    # Blueprints

    app.register_blueprint(candidates_blueprint)

    # Flask admin

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='admin', template_mode='bootstrap3')

    from cowork_site.models import Candidate

    admin.add_view(ModelView(Candidate, app.session_factory))

    @app.errorhandler(Exception)
    def handle_unknown_error(error):
        app.logger.exception(error)
        if isinstance(error, HTTPException):
            return error
        abort(500)

    return app
