from sqlalchemy import orm

sqla_session_factory = orm.scoped_session(orm.sessionmaker())
