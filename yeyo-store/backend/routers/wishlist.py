"""
Rutas de lista de deseos (wishlist)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies.auth import get_current_user_id
from dependencies.exceptions import ProductoNoEncontrado
from schemas.lista_deseos import ListaDeseosResponse, ListaDeseosCreate
from services.lista_deseos_service import ListaDeseosService
from db.connection import get_session

router = APIRouter(prefix="/api/wishlist", tags=["wishlist"])


@router.post("", response_model=ListaDeseosResponse, status_code=201)
def add_to_wishlist(
    lista_create: ListaDeseosCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Agregar un producto a la lista de deseos
    """
    try:
        wishlist_service = ListaDeseosService(session)
        item = wishlist_service.agregar_a_wishlist(
            user_id=current_user_id,
            producto_id=lista_create.id_producto,
        )
        return item
    except ValueError as e:
        if "ya existe" in str(e).lower():
            raise HTTPException(
                status_code=409,
                detail="El producto ya está en tu lista de deseos",
            )
        raise ProductoNoEncontrado(detail=str(e))


@router.get("", response_model=list[ListaDeseosResponse])
def get_wishlist(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Obtener la lista de deseos del usuario actual
    """
    try:
        wishlist_service = ListaDeseosService(session)
        items = wishlist_service.obtener_wishlist_usuario(current_user_id)
        return items
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{lista_deseos_id}")
def remove_from_wishlist(
    lista_deseos_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Remover un producto de la lista de deseos
    """
    try:
        wishlist_service = ListaDeseosService(session)
        item = wishlist_service.obtener_item_wishlist(lista_deseos_id)
        
        # Verificar que el item pertenece al usuario actual
        if item.id_usuario != current_user_id:
            raise HTTPException(status_code=403, detail="No autorizado")
        
        wishlist_service.remover_de_wishlist(
            user_id=current_user_id,
            producto_id=item.id_producto,
        )
        return {"message": "Producto removido de la lista de deseos"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("")
def clear_wishlist(
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Limpiar toda la lista de deseos del usuario actual
    """
    try:
        wishlist_service = ListaDeseosService(session)
        count = wishlist_service.limpiar_wishlist(current_user_id)
        return {"message": f"Se removieron {count} productos de la lista de deseos"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

