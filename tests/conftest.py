import os
import pytest
from cowork_site.app import create_app
from cowork_site.db import get_db_engine

from .common import sqla_session_factory


@pytest.fixture(scope="function")
def config(monkeypatch):
    from cowork_site.config import Configuration

    class TestConfig(Configuration):
        pass

    TestConfig.TESTING = True
    TestConfig.DEBUG = True
    TestConfig.CACHE_TYPE = 'NULL'

    monkeypatch.setattr('cowork_site.config.Configuration', TestConfig)
    return TestConfig


@pytest.fixture(scope="function")
def engine(config):
    db_url = config.SQLALCHEMY_URL
    assert 'test' in db_url
    engine = get_db_engine(db_url, config.DB_ECHO)
    return engine


@pytest.yield_fixture(scope="function")
def connection(engine):
    connection = engine.connect()
    transaction = connection.begin()
    yield connection
    transaction.close()
    connection.close()


@pytest.yield_fixture(scope="function")
def session_factory(connection, monkeypatch):
    # Bind factories to this session maker
    sqla_session_factory.configure(bind=connection)
    db_session_factory = sqla_session_factory

    def mock_get_db_session_factory(*args):
        return db_session_factory

    yield db_session_factory
    db_session_factory.remove()


@pytest.yield_fixture(scope="function")
def session(session_factory):
    session = session_factory()
    session.expire_on_commit = False
    yield session
    session.close()


@pytest.fixture
def app(session_factory, config):
    app = create_app(config=config, session_factory=session_factory)
    return app


@pytest.fixture(scope='function')
def app_factory(session_factory, config):
    def _make_app():
        app = create_app(config=config, session_factory=session_factory)
        return app, app.test_client()
    return _make_app


@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        return client
