# src/api/v1/contact.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...dependencies import get_db
from ...schemas.contact import ContactCreate, ContactResponse
from ...crud.lead import get_or_create_lead
from ...crud.source import get_source_by_name
from ...services.distribution import select_operator
from ...models import Contact

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact_in: ContactCreate, db: Session = Depends(get_db)):
    # 1. Находим или создаём лида
    lead = get_or_create_lead(db, contact_in.external_id)

    # 2. Находим источник
    source = get_source_by_name(db, contact_in.source_name)
    if not source:
        raise HTTPException(404, f"Источник '{contact_in.source_name}' не найден")

    # 3. Выбираем оператора (вот она — магия!)
    operator = select_operator(db, source.id)

    # 4. Создаём обращение
    contact = Contact(
        lead_id=lead.id,
        source_id=source.id,
        operator_id=operator.id if operator else None,
        payload=contact_in.payload,
        is_active=True,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return ContactResponse(
        id=contact.id,
        lead_id=contact.lead_id,
        source_name=source.name,
        operator_name=operator.name if operator else None,
        is_active=contact.is_active,
        created_at=contact.created_at,
    )
    
@router.get("/", response_model=list[ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).order_by(Contact.created_at.desc()).all()
    return [
        ContactResponse(
            id=c.id,
            lead_id=c.lead_id,
            source_name=c.source.name,
            operator_name=c.operator.name if c.operator else None,
            is_active=c.is_active,
            created_at=c.created_at,
        )
        for c in contacts
    ]    