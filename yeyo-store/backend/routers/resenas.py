"""
Rutas de reseñas y calificaciones
"""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from dependencies.auth import get_current_user_id
from dependencies.exceptions import (
    ProductoNoEncontrado,
    ReseñaYaExiste,
    NoAutorizado,
)
from schemas.reseña import ReseñaResponse, ReseñaCreate, ReseñaUpdate
from services.reseña_service import ReseñaService
from db.connection import get_session

router = APIRouter(prefix="/api/productos", tags=["resenas"])


@router.post("/{producto_id}/resenas", response_model=ReseñaResponse, status_code=201)
def create_review(
    producto_id: int,
    reseña_create: ReseñaCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Crear una nueva reseña para un producto
    - calificacion: 1-5
    - titulo: Título de la reseña
    - comentario: Descripción detallada
    """
    try:
        reseña_service = ReseñaService(session)
        reseña = reseña_service.crear_reseña(
            user_id=current_user_id,
            producto_id=producto_id,
            reseña_create=reseña_create,
        )
        return reseña
    except ValueError as e:
        if "ya existe" in str(e).lower():
            raise ReseñaYaExiste(detail=str(e))
        raise ProductoNoEncontrado(detail=str(e))


@router.get("/{producto_id}/resenas", response_model=list[ReseñaResponse])
def get_product_reviews(
    producto_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """
    Obtener todas las reseñas de un producto
    """
    try:
        reseña_service = ReseñaService(session)
        reseñas = reseña_service.obtener_reseñas_producto(
            producto_id=producto_id,
            skip=skip,
            limit=limit,
        )
        return reseñas
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.get("/resenas/{reseña_id}", response_model=ReseñaResponse)
def get_review(
    reseña_id: int,
    session: Session = Depends(get_session),
):
    """
    Obtener una reseña específica
    """
    try:
        reseña_service = ReseñaService(session)
        reseña = reseña_service.obtener_reseña(reseña_id)
        return reseña
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.put("/resenas/{reseña_id}", response_model=ReseñaResponse)
def update_review(
    reseña_id: int,
    reseña_update: ReseñaUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Actualizar una reseña (solo el autor)
    """
    try:
        reseña_service = ReseñaService(session)
        
        # Verificar que la reseña pertenece al usuario actual
        reseña_original = reseña_service.obtener_reseña(reseña_id)
        if reseña_original.id_usuario != current_user_id:
            raise NoAutorizado()
        
        reseña = reseña_service.actualizar_reseña(
            reseña_id=reseña_id,
            reseña_update=reseña_update,
        )
        return reseña
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.delete("/resenas/{reseña_id}")
def delete_review(
    reseña_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Eliminar una reseña (solo el autor)
    """
    try:
        reseña_service = ReseñaService(session)
        
        # Verificar que la reseña pertenece al usuario actual
        reseña = reseña_service.obtener_reseña(reseña_id)
        if reseña.id_usuario != current_user_id:
            raise NoAutorizado()
        
        reseña_service.eliminar_reseña(reseña_id)
        return {"message": "Reseña eliminada exitosamente"}
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))

