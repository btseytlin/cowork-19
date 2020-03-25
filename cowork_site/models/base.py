from sqlalchemy_searchable import make_searchable
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

make_searchable(Base.metadata)