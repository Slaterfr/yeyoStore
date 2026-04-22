"""
Configuración centralizada del backend YeYo Store
Soporta variables de entorno para desarrollo, testing y producción
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Configuración de la aplicación
    Las variables se cargan desde .env o variables de entorno del sistema
    """

    # =====================================================================
    # CONFIGURACIÓN DE BASE DE DATOS
    # =====================================================================
    DATABASE_URL: str = ""
    SQLALCHEMY_ECHO: bool = False  # Log SQL queries en desarrollo

    # =====================================================================
    # CONFIGURACIÓN JWT / AUTENTICACIÓN
    # =====================================================================
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutos
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 días

    # =====================================================================
    # CONFIGURACIÓN DE LA APLICACIÓN
    # =====================================================================
    APP_NAME: str = "YeYo Store API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development, testing, production

    # =====================================================================
    # CONFIGURACIÓN CORS
    # =====================================================================
    CORS_ORIGINS: list[str] = ["*"]  # En producción: restricción de orígenes
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    # =====================================================================
    # CONFIGURACIÓN DE FOTOS / CLOUDINARY
    # =====================================================================
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None

    # =====================================================================
    # CONFIGURACIÓN DE PAGOS (futuro)
    # =====================================================================
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLIC_KEY: Optional[str] = None

    # =====================================================================
    # RUTAS DEL PROYECTO
    # =====================================================================
    BASE_DIR: Path = Path(__file__).parent.parent
    FRONTEND_DIR: Path = BASE_DIR / "frontend"
    STATIC_DIR: Path = BASE_DIR / "frontend"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instancia global de settings
settings = Settings()


# Validaciones en función del entorno
if not settings.DATABASE_URL:
    raise ValueError("❌ ERROR: DATABASE_URL no está configurada. Define DATABASE_URL en variables de entorno.")

if settings.ENVIRONMENT == "production":
    if "localhost" in settings.DATABASE_URL or "127.0.0.1" in settings.DATABASE_URL:
        raise ValueError("❌ ERROR: En producción DATABASE_URL no puede apuntar a localhost.")
    assert settings.SECRET_KEY != "your-super-secret-key-change-in-production", \
        "❌ ERROR: Cambiar SECRET_KEY en producción"
    assert not settings.DEBUG, "❌ ERRO R: DEBUG=False requerido en producción"
    assert not settings.SQLALCHEMY_ECHO, "❌ ERROR: SQLALCHEMY_ECHO=False requerido en producción"
