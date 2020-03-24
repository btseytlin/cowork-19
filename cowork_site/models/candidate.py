from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Enum, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from .base import Base


class Candidate(Base):
    __tablename__ = 'candidate'

    id = Column(UUID, primary_key=True, default=lambda: str(uuid4()), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    display = Column(Boolean, default=True)

    name = Column(String)
    description = Column(String)
    email = Column(String)
    cv_url = Column(String)
