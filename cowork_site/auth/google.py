from flask import flash, g, current_app
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound

from cowork_site.models.auth import User, OAuth
from cowork_site.db import GLOBAL_SESSION_FACTORY
from cowork_site import config

google_auth_blueprint = make_google_blueprint(
    client_id=config.Configuration.GOOGLE_CLIENT_ID,
    client_secret=config.Configuration.GOOGLE_CLIENT_SECRET,
    scope=["openid",
           "https://www.googleapis.com/auth/userinfo.email",
           "https://www.googleapis.com/auth/userinfo.profile"],
    storage=SQLAlchemyStorage(OAuth, GLOBAL_SESSION_FACTORY, user=current_user),
)


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_auth_blueprint)
def google_logged_in(google_auth_blueprint, token):
    s = current_app.session_factory()

    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = google_auth_blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    info = resp.json()
    print('USERINFO', info)
    user_id = info["id"]

    # Find this OAuth token in the database, or create it
    query = s.query(OAuth).filter_by(provider=google_auth_blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=google_auth_blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.")

    else:

        # Create a new local user account for this user
        user = User(email=info["email"])
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        s.add(user)
        s.add(oauth)
        s.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(google_auth_blueprint)
def google_error(google_auth_blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=google_auth_blueprint.name, message=message, response=response
    )
    flash(msg, category="error")