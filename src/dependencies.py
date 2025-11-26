# src/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .core.config import settings

__all__ = ["get_db", "settings"]