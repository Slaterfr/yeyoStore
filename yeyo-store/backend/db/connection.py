"""
Configuración de conexión a PostgreSQL
Engine, SessionLocal y otras utilidades de BD
"""
from sqlmodel import create_engine, Session, SQLModel
from config import settings
import logging

logger = logging.getLogger(__name__)

# Crear engine con PostgreSQL
# pool_pre_ping=True: verifica conexión antes de usarla
# echo=settings.SQLALCHEMY_ECHO: loguea SQL queries
try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.SQLALCHEMY_ECHO,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )
except Exception as e:
    logger.error(f"❌ Error al crear engine de SQLAlchemy: {e}")
    logger.error(f"   DATABASE_URL: {settings.DATABASE_URL}")
    logger.error(f"   Por favor verifica que PostgreSQL está corriendo y las credenciales son correctas")
    raise


def create_db_and_tables():
    """
    Crea todas las tablas en la base de datos
    Se llama en el lifespan startup de FastAPI
    """
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        logger.error(f"   Verifica que:")
        logger.error(f"   - PostgreSQL está corriendo en {settings.DATABASE_URL.split('@')[1]}")
        logger.error(f"   - La base de datos existe")
        logger.error(f"   - Las credenciales son correctas")
        raise


def get_session():
    """
    Dependency para inyectar sesión en routers
    Uso en FastAPI:
        from db.connection import get_session
        
        @app.get("/items/")
        def read_items(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session
