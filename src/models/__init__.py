# src/models/__init__.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON, func, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base


# ----------------------- БАЗОВЫЙ КЛАСС -----------------------
class TimeStampedModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


# ----------------------- ОСНОВНЫЕ МОДЕЛИ -----------------------
class Lead(TimeStampedModel):
    __tablename__ = "leads"

    external_id = Column(String, unique=True, nullable=False, index=True)

    contacts = relationship("Contact", back_populates="lead", cascade="all, delete-orphan")


class Source(TimeStampedModel):
    __tablename__ = "sources"

    name = Column(String, unique=True, nullable=False, index=True)

    operator_weights = relationship("SourceOperatorWeight", back_populates="source", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="source")


class Operator(TimeStampedModel):
    __tablename__ = "operators"

    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    max_active_contacts = Column(Integer, default=50)

    source_weights = relationship("SourceOperatorWeight", back_populates="operator", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="operator")


class SourceOperatorWeight(TimeStampedModel):
    __tablename__ = "source_operator_weights"

    source_id = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Integer, nullable=False, default=10)

    __table_args__ = (UniqueConstraint("source_id", "operator_id", name="uix_source_operator"),)

    source = relationship("Source", back_populates="operator_weights")
    operator = relationship("Operator", back_populates="source_weights")


class Contact(TimeStampedModel):
    __tablename__ = "contacts"

    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id", ondelete="SET NULL"), nullable=True)

    is_active = Column(Boolean, default=True)
    payload = Column(JSON, nullable=True)

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")