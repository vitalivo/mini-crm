# src/models/base.py
from sqlalchemy import Column, Integer, DateTime, Boolean, func
from ..database import Base


class TimeStampedModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)