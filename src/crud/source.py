# src/crud/source.py
from sqlalchemy.orm import Session
from ..models import Source


def get_source_by_name(db: Session, name: str) -> Source:
    return db.query(Source).filter(Source.name == name).first()