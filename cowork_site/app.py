from flask import Flask, abort, flash, redirect, url_for, render_template
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

from cowork_site.admin import AdminModelView, ProtectedIndexView
from cowork_site.postings.blueprint import postings_blueprint


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
        return redirect(url_for("postings.posting_list"))


    # Flask admin

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='admin', index_view=ProtectedIndexView(), template_mode='bootstrap3')

    from cowork_site.models import Posting

    admin.add_view(AdminModelView(Posting, app.session_factory))

    # App blueprints

    app.register_blueprint(postings_blueprint)

    @app.errorhandler(Exception)
    def handle_unknown_error(error):
        app.logger.exception(error)
        if isinstance(error, HTTPException):
            return error
        abort(500)

    # Sentry
    if config.SENTRY_DSD:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(
            dsn=config.SENTRY_DSD,
            integrations=[FlaskIntegration()]
        )

    @app.route("/about")
    def about():
        return render_template('about.html')

    return app
