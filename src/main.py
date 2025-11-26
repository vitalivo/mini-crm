# src/main.py
from fastapi import FastAPI
from .core.config import settings
from .database import engine, Base

# ← ВСЁ, что нужно из моделей — уже импортируется через models/__init__.py
from .models import *  # ← этот импорт регистрирует ВСЕ модели

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Тестовое задание: мини-CRM с умным распределением лидов",
    openapi_url="/openapi.json",
    docs_url="/docs",
)


@app.get("/")
async def root():
    return {
        "message": "Mini CRM работает!",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    # Больше никаких импортов не нужно — все модели уже загружены через from .models import *
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы (или уже существуют)")
    
from .api.v1.admin import router as admin_router
from .api.v1.contact import router as contact_router

app.include_router(admin_router)
app.include_router(contact_router)    