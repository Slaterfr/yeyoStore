"""
Rutas de tallas de zapatos
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from services.talla_service import TallaService
from db.connection import get_session
from schemas.talla import TallaResponse

router = APIRouter(prefix="/api/tallas", tags=["tallas"])


@router.get("", response_model=list[TallaResponse])
def get_all_tallas(
    session: Session = Depends(get_session),
):
    """
    Obtener todas las tallas disponibles
    """
    try:
        talla_service = TallaService(session)
        tallas = talla_service.obtener_todas_las_tallas()
        return tallas
    except ValueError as e:
        raise ValueError(str(e))
