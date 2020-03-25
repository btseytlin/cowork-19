from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flask import current_app

from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from .base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(UUID, primary_key=True, default=lambda: str(uuid4()), index=True)
    email = Column(String(256), unique=True)


class OAuth(OAuthConsumerMixin, Base):
    __tablename__ = 'oauth'

    provider_user_id = Column(String(256), unique=True, nullable=False)
    user_id = Column(UUID, ForeignKey(User.id), nullable=False)
    user = relationship(User)


# setup login manager
login_manager = LoginManager()
login_manager.login_view = "google.login"


@login_manager.user_loader
def load_user(user_id):
    s = current_app.session_factory()
    return s.query(User).get(user_id)