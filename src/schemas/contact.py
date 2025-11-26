# src/schemas/contact.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ContactCreate(BaseModel):
    external_id: str
    source_name: str
    payload: Optional[Dict[str, Any]] = None


class ContactResponse(BaseModel):
    id: int
    lead_id: int
    source_name: str
    operator_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True