from fastapi import APIRouter
from app.api.v1.endpoints import categories, documents

api_router = APIRouter()

api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
