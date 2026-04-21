"""
Rutas de usuarios y direcciones
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies.auth import get_current_user_id
from dependencies.exceptions import UsuarioNoEncontrado, NoAutorizado
from schemas.usuario import UsuarioResponse, UsuarioUpdate
from schemas.direccion import DireccionCreate, DireccionResponse, DireccionUpdate
from services.user_service import UserService
from services.direccion_service import DireccionService
from db.connection import get_session

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Obtener información del usuario actual
    """
    try:
        user_service = UserService(session)
        usuario = user_service.obtener_usuario(current_user_id)
        return usuario
    except ValueError as e:
        raise UsuarioNoEncontrado(detail=str(e))


@router.put("/me", response_model=UsuarioResponse)
def update_current_user(
    usuario_update: UsuarioUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Actualizar información del usuario actual
    """
    try:
        user_service = UserService(session)
        usuario = user_service.actualizar_usuario(
            user_id=current_user_id,
            usuario_update=usuario_update,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/me/deactivate")
def deactivate_account(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Desactivar cuenta del usuario actual
    """
    try:
        user_service = UserService(session)
        user_service.desactivar_usuario(current_user_id)
        return {"message": "Cuenta desactivada exitosamente"}
    except ValueError as e:
        raise UsuarioNoEncontrado(detail=str(e))


@router.post("/me/direcciones", response_model=DireccionResponse)
def create_address(
    direccion_create: DireccionCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Crear una nueva dirección para el usuario actual
    """
    try:
        direccion_service = DireccionService(session)
        direccion = direccion_service.crear_direccion(
            user_id=current_user_id,
            direccion_create=direccion_create,
        )
        return direccion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me/direcciones", response_model=list[DireccionResponse])
def get_user_addresses(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Obtener todas las direcciones del usuario actual
    """
    try:
        direccion_service = DireccionService(session)
        direcciones = direccion_service.obtener_direcciones_usuario(
            current_user_id
        )
        return direcciones
    except ValueError as e:
        raise UsuarioNoEncontrado(detail=str(e))


@router.get("/me/direcciones/{direccion_id}", response_model=DireccionResponse)
def get_user_address(
    direccion_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Obtener una dirección específica del usuario actual
    """
    try:
        direccion_service = DireccionService(session)
        direccion = direccion_service.obtener_direccion(direccion_id)
        
        # Verificar que la dirección pertenece al usuario actual
        if direccion.id_usuario != current_user_id:
            raise NoAutorizado()
        
        return direccion
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/me/direcciones/{direccion_id}", response_model=DireccionResponse)
def update_user_address(
    direccion_id: int,
    direccion_update: DireccionUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Actualizar una dirección del usuario actual
    """
    try:
        direccion_service = DireccionService(session)
        
        # Verificar que la dirección pertenece al usuario actual
        direccion_original = direccion_service.obtener_direccion(direccion_id)
        if direccion_original.id_usuario != current_user_id:
            raise NoAutorizado()
        
        direccion = direccion_service.actualizar_direccion(
            direccion_id=direccion_id,
            direccion_update=direccion_update,
        )
        return direccion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/me/direcciones/{direccion_id}")
def delete_user_address(
    direccion_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Eliminar una dirección del usuario actual
    """
    try:
        direccion_service = DireccionService(session)
        
        # Verificar que la dirección pertenece al usuario actual
        direccion = direccion_service.obtener_direccion(direccion_id)
        if direccion.id_usuario != current_user_id:
            raise NoAutorizado()
        
        direccion_service.eliminar_direccion(direccion_id)
        return {"message": "Dirección eliminada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

