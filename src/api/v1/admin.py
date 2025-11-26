# src/api/v1/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from ...dependencies import get_db
from ...models import Operator, Source, SourceOperatorWeight


router = APIRouter(prefix="/admin", tags=["admin"])


# === СХЕМЫ ===
class OperatorCreate(BaseModel):
    name: str
    max_active: int = 50


class SourceCreate(BaseModel):
    name: str


class WeightsUpdate(BaseModel):
    weights: Dict[int, int]  # {operator_id: weight}


# === ЭНДПОИНТЫ ===
@router.post("/operators/", response_model=dict)
def create_operator(payload: OperatorCreate, db: Session = Depends(get_db)):
    op = Operator(name=payload.name, max_active_contacts=payload.max_active)
    db.add(op)
    db.commit()
    db.refresh(op)
    return {"id": op.id, "name": op.name}


@router.post("/sources/", response_model=dict)
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    if db.query(Source).filter(Source.name == payload.name).first():
        raise HTTPException(400, "Источник уже существует")
    src = Source(name=payload.name)
    db.add(src)
    db.commit()
    db.refresh(src)
    return {"id": src.id, "name": src.name}


@router.post("/sources/{source_name}/weights")
def set_weights(source_name: str, payload: WeightsUpdate, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.name == source_name).first()
    if not source:
        raise HTTPException(404, "Источник не найден")

    db.query(SourceOperatorWeight).filter(SourceOperatorWeight.source_id == source.id).delete()

    for op_id, weight in payload.weights.items():
        if weight <= 0:
            continue
        db.add(SourceOperatorWeight(source_id=source.id, operator_id=op_id, weight=weight))

    db.commit()
    return {"status": "ok", "source": source_name, "weights_set": len(payload.weights)}