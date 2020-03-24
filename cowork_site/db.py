import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from cowork_site.models import Base

# Postgres unique code error
UNIQUE_CODE_ERROR = "23505"


def get_db_engine(db_uri, echo=False):
    engine = create_engine(db_uri, convert_unicode=True, echo=echo)
    return engine


def get_db_session_factory(engine):
    session_maker = sessionmaker(autocommit=False, autoflush=False)
    session_maker.configure(bind=engine)
    return scoped_session(session_maker)


def create_tables(engine):
    from .models import Base
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_context(engine):
    """Provide a transactional scope around a series of operations."""
    session = get_db_session_factory(engine)
    try:
        yield session
    except Exception:
        logging.info("Session rollback.")
        session.rollback()
        raise
    finally:
        logging.info("Closing db connection.")
        session.close()
        logging.info("Removing session.")
        session.remove()


def configure_database(app,
                       sqla_url,
                       db_echo,
                       session_factory):
    app.engine = get_db_engine(sqla_url,
                           echo=db_echo)
    app.session_factory = session_factory or get_db_session_factory(app.engine)
    Base.metadata.bind = app.session_factory

    @app.teardown_appcontext
    def close_db_session(error):
        if getattr(app, 'session_factory') and app.session_factory:
            try:
                if error:
                    app.logger.debug("Session rollback")
                    app.session_factory.rollback()
            finally:
                app.logger.debug("Removing session")
                app.session_factory.close()
        app.logger.debug("Closing db connection...")
        app.session_factory.remove()
        app.logger.debug("Closed db connection")
