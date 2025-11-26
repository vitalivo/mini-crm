# src/schemas/weight.py
from pydantic import BaseModel
from typing import Dict


class WeightsUpdate(BaseModel):
    weights: Dict[int, int]   # {operator_id: weight}