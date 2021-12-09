from fastapi import APIRouter

from routes import log_errores

api_router = APIRouter()
api_router.include_router(log_errores.router, tags=["pruebas"], prefix="/base")