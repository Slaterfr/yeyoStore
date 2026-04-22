"""
YeYo Store - Backend Principal
FastAPI + PostgreSQL + SQLModel

Punto de entrada de la aplicación
Configuración de middleware, routers y eventos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
from contextlib import asynccontextmanager

# Import de configuración
from config import settings
from db.connection import create_db_and_tables, get_session

# ============================================================================
# LIFESPAN EVENTS (Startup/Shutdown)
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de eventos del ciclo de vida de la aplicación
    - Startup: Inicializar base de datos
    - Shutdown: Limpiar recursos
    """
    # === STARTUP ===
    print("🚀 Iniciando YeYo Store API...")
    print(f"   Entorno: {settings.ENVIRONMENT}")
    print(f"   Debug: {settings.DEBUG}")
    
    try:
        create_db_and_tables()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error crítico al inicializar base de datos:")
        print(f"   {type(e).__name__}: {e}")
        print("")
        print("📋 SOLUCIÓN:")
        print("   1. Verifica que PostgreSQL está corriendo")
        print("   2. Comprueba que la BD 'yeyo_store' existe:")
        print("      psql -U postgres -c \"CREATE DATABASE yeyo_store;\"")
        print("   3. Verifica credenciales en backend/.env")
        print("   4. Asegúrate de NO usar caracteres especiales (ó, á, etc)")
        print("      en la contraseña de PostgreSQL")
        raise
    
    yield
    
    # === SHUTDOWN ===
    print("🛑 Apagando YeYo Store API...")


# ============================================================================
# INICIALIZAR APP
# ============================================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# ============================================================================
# MIDDLEWARE CORS
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=['*'],
    allow_headers=settings.CORS_HEADERS,
)

# ============================================================================
# ROUTERS
# ============================================================================

from routers import auth, usuarios, productos, ordenes, resenas, wishlist, cupones, tallas, admin, health

app.include_router(health.router)
app.include_router(auth.router, tags=["auth"])
app.include_router(usuarios.router, tags=["usuarios"])
app.include_router(productos.router, tags=["productos"])
app.include_router(tallas.router, tags=["tallas"])
app.include_router(resenas.router, tags=["resenas"])
app.include_router(wishlist.router, tags=["wishlist"])
app.include_router(cupones.router, tags=["cupones"])
app.include_router(ordenes.router, tags=["ordenes"])
app.include_router(admin.router, tags=["admin"])


# ============================================================================
# STATIC FILES / FRONTEND
# ============================================================================

# Servir archivos estáticos del frontend
frontend_dir = settings.STATIC_DIR
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
async def root():
    """Retorna el index.html del frontend"""
    index_path = settings.FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "YeYo Store API - Frontend no encontrado"}


# ============================================================================
# HEALTH CHECK
# ============================================================================


@app.get("/health")
async def health_check():
    """Verificar que la API está funcionando"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# ============================================================================
# DOCUMENTACIÓN AUTOMÁTICA
# ============================================================================

# Swagger UI disponible en: http://localhost:8000/docs
# ReDoc disponible en: http://localhost:8000/redoc

# ============================================================================
# ENDPOINTS API
# ============================================================================


# ============================================================================
# SERVIR FRONTEND COMO ARCHIVOS ESTÁTICOS
# ============================================================================

frontend_path = Path(__file__).parent.parent / "frontend"

@app.get("/")
async def serve_index():
    """Sirve el index.html si existe; fallback a estado de API en backend-only deploy."""
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "status": "ok",
        "message": "YeYo Store API running",
        "docs": "/docs",
    }

# Montar frontend solo si la carpeta existe (evita crash en Render backend-only)
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
