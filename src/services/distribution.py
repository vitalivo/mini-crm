# src/services/distribution.py
import random
from typing import Optional
from sqlalchemy.orm import Session
from ..models import SourceOperatorWeight, Operator, Contact


def get_available_operators(db: Session, source_id: int):
    """Возвращает список (weight_obj, operator) для доступных операторов"""
    weights = (
        db.query(SourceOperatorWeight)
        .filter(SourceOperatorWeight.source_id == source_id)
        .all()
    )

    candidates = []
    weights_list = []

    for weight_obj in weights:
        op: Operator = weight_obj.operator

        if not op.is_active:
            continue

        # Считаем текущую нагрузку
        current_load = (
            db.query(Contact)
            .filter(Contact.operator_id == op.id, Contact.is_active == True)
            .count()
        )

        if current_load >= op.max_active_contacts:
            continue

        candidates.append(weight_obj)      # сохраняем объект с весом
        weights_list.append(weight_obj.weight)

    return candidates, weights_list


def select_operator(db: Session, source_id: int) -> Optional[Operator]:
    """
    Главная магия: выбирает оператора по весам с учётом лимитов
    Возвращает Operator или None
    """
    candidates, weights_list = get_available_operators(db, source_id)

    if not candidates:
        return None

    # Взвешенный случайный выбор — идеально сходится к заданным пропорциям
    chosen_weight_obj = random.choices(candidates, weights=weights_list, k=1)[0]
    return chosen_weight_obj.operator