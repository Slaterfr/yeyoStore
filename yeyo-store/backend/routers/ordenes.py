"""
Rutas de órdenes y pagos
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from typing import Optional

from dependencies.auth import get_current_user_id
from dependencies.exceptions import (
    PedidoNoEncontrado,
    CuponInvalido,
    ProductoNoEncontrado,
    StockInsuficiente,
)
from schemas.pedido import PedidoResponse, PedidoCreate
from services.pedido_service import PedidoService
from services.cupon_service import CuponService
from services.producto_service import ProductoService
from db.connection import get_session

router = APIRouter(prefix="/api/ordenes", tags=["ordenes"])


@router.post("", response_model=PedidoResponse, status_code=201)
def create_order(
    pedido_create: PedidoCreate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Crear una nueva orden
    
    Body:
    - id_direccion_envio: ID de la dirección de envío (obtenida del usuario)
    - items: Lista de {id_producto, cantidad, precio_unitario}
    - codigo_cupon: Código de cupón (opcional)
    
    Proceso:
    1. Validar que existan los productos
    2. Validar que haya stock suficiente
    3. Validar cupón si se proporcionó
    4. Crear pedido con estado 'pendiente'
    5. Decrementar stock de productos
    """
    try:
        pedido_service = PedidoService(session)
        
        # Aplicar cupón si se proporciona
        cupon = None
        if pedido_create.codigo_cupon_aplicado:
            cupon_service = CuponService(session)
            try:
                cupon = cupon_service.aplicar_cupon(pedido_create.codigo_cupon_aplicado)
            except ValueError as e:
                raise CuponInvalido(detail=str(e))
        
        # Crear pedido
        pedido = pedido_service.crear_pedido(
            user_id=current_user_id,
            pedido_create=pedido_create,
            cupon=cupon,
        )
        return pedido
    except ValueError as e:
        error_msg = str(e).lower()
        if "stock" in error_msg:
            raise StockInsuficiente(detail=str(e))
        elif "producto" in error_msg or "no encontrado" in error_msg:
            raise ProductoNoEncontrado(detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[PedidoResponse])
def get_user_orders(
    current_user_id: int = Depends(get_current_user_id),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    estado: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    """
    Obtener todas las órdenes del usuario actual
    - estado: Filtrar por estado (pendiente, completada, cancelada, etc.)
    """
    try:
        pedido_service = PedidoService(session)
        pedidos = pedido_service.obtener_pedidos_usuario(
            user_id=current_user_id,
            skip=skip,
            limit=limit,
            estado_filtro=estado,
        )
        return pedidos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pedido_id}", response_model=PedidoResponse)
def get_order(
    pedido_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Obtener detalles de una orden específica
    """
    try:
        pedido_service = PedidoService(session)
        pedido = pedido_service.obtener_pedido(pedido_id)
        
        # Verificar que la orden pertenece al usuario actual
        if pedido.id_usuario != current_user_id:
            raise HTTPException(status_code=403, detail="No autorizado")
        
        return pedido
    except ValueError as e:
        raise PedidoNoEncontrado(detail=str(e))


@router.put("/{pedido_id}/cancelar")
def cancel_order(
    pedido_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Cancelar una orden (solo si está en estado 'pendiente')
    """
    try:
        pedido_service = PedidoService(session)
        pedido = pedido_service.obtener_pedido(pedido_id)
        
        # Verificar que la orden pertenece al usuario actual
        if pedido.id_usuario != current_user_id:
            raise HTTPException(status_code=403, detail="No autorizado")
        
        # Cancelar orden
        resultado = pedido_service.cancelar_pedido(pedido_id)
        return {"message": "Orden cancelada exitosamente", "data": resultado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pedido_id}/rastreo")
def track_order(
    pedido_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Obtener información de rastreo de una orden
    """
    try:
        pedido_service = PedidoService(session)
        pedido = pedido_service.obtener_pedido(pedido_id)
        
        # Verificar que la orden pertenece al usuario actual
        if pedido.id_usuario != current_user_id:
            raise HTTPException(status_code=403, detail="No autorizado")
        
        # Obtener información de rastreo
        rastreo = pedido_service.obtener_rastreo_pedido(pedido_id)
        return rastreo
    except ValueError as e:
        raise PedidoNoEncontrado(detail=str(e))

