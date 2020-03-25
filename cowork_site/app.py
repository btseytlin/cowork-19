from flask import Flask, abort, flash, redirect, url_for
from flask.logging import default_handler
from werkzeug.exceptions import HTTPException


from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, logout_user


from cowork_site import config
from cowork_site.utils import configure_logger
from cowork_site.db import configure_database
from cowork_site.models.auth import login_manager
from cowork_site.auth.google import google_auth_blueprint

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


    # OAuth

    app.register_blueprint(google_auth_blueprint, url_prefix="/login")

    login_manager.init_app(app)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have logged out")
        return redirect(url_for("candidates.candidate_list"))


    # Flask admin

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='admin', template_mode='bootstrap3')

    from cowork_site.models import Candidate

    admin.add_view(ModelView(Candidate, app.session_factory))

    # App blueprints

    app.register_blueprint(candidates_blueprint)

    @app.errorhandler(Exception)
    def handle_unknown_error(error):
        app.logger.exception(error)
        if isinstance(error, HTTPException):
            return error
        abort(500)

    return app
