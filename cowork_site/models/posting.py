from datetime import datetime
from uuid import uuid4
from sqlalchemy import (Column, String, Text, Enum, Integer, ForeignKey, DateTime,
                        Boolean, Index, func, text, cast)
from sqlalchemy.dialects.postgresql import JSONB, UUID, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import TSVectorType
from .base import Base


class Posting(Base):
    __tablename__ = 'posting'
    __searchable__ = ['name', 'description']

    id = Column(UUID, primary_key=True, default=lambda: str(uuid4()), index=True)
    user_id = Column(UUID, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    display = Column(Boolean, default=True)

    name = Column(String)
    description = Column(Text)
    cv_url = Column(String)

    search_vector = Column(TSVectorType('name', 'description'))

    user = relationship("User", backref="postings")