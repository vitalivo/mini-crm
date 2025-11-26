# src/crud/lead.py
from sqlalchemy.orm import Session
from ..models import Lead


def get_or_create_lead(db: Session, external_id: str) -> Lead:
    lead = db.query(Lead).filter(Lead.external_id == external_id).first()
    if not lead:
        lead = Lead(external_id=external_id)
        db.add(lead)
        db.commit()
        db.refresh(lead)
    return lead