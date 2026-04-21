"""
Rutas de Health Check y Status
Para verificar que la aplicación está corriendo correctamente
"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    """
    Health check endpoint para Docker y load balancers
    Retorna status si la aplicación está corriendo
    """
    return {
        "status": "healthy",
        "message": "YeYo Store API is running",
        "version": "1.0.0"
    }

@router.get("/api/health")
def api_health():
    """
    Health check para API específicamente
    """
    return {
        "status": "ok",
        "service": "yeyo-store-api"
    }
