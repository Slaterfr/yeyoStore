"""
Rutas administrativas
Solo accesibles por usuarios con rol admin
"""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from decimal import Decimal

from dependencies.auth import require_role
from db.connection import get_session
from services.producto_service import ProductoService
from schemas.producto import ProductoResponse, ProductoUpdate

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/inventario", response_model=list[ProductoResponse])
def get_inventory(
    user_data: dict = Depends(require_role("admin")),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    """
    Obtener inventario completo de productos
    Solo accesible por administradores
    
    Muestra:
    - Todos los productos
    - Stock disponible
    - Precios
    - Detalles
    """
    try:
        producto_service = ProductoService(session)
        productos = producto_service.obtener_todos_productos(skip=skip, limit=limit)
        return productos
    except ValueError as e:
        raise ValueError(str(e))


@router.get("/inventario/search")
def search_inventory(
    user_data: dict = Depends(require_role("admin")),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    min_stock: Optional[int] = Query(None, description="Stock mínimo"),
    max_stock: Optional[int] = Query(None, description="Stock máximo"),
    session: Session = Depends(get_session),
):
    """
    Buscar productos en inventario
    Filtros: nombre, rango de stock
    """
    try:
        from sqlmodel import select
        from models.producto import Producto
        
        query = select(Producto)
        
        if q:
            query = query.where(
                (Producto.nombre_producto.contains(q)) |
                (Producto.descripcion_producto.contains(q))
            )
        
        if min_stock is not None:
            query = query.where(Producto.stock_producto >= min_stock)
        
        if max_stock is not None:
            query = query.where(Producto.stock_producto <= max_stock)
        
        productos = session.exec(query).all()
        return {
            "total": len(productos),
            "productos": productos
        }
    except Exception as e:
        raise ValueError(f"Error en búsqueda: {str(e)}")


@router.put("/productos/{producto_id}")
def update_product(
    producto_id: int,
    producto_update: ProductoUpdate,
    user_data: dict = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """
    Actualizar detalles de un producto
    Solo accesible por administradores
    
    - stock_producto: Cantidad disponible
    - precio_producto: Precio en colones
    - nombre_producto: Nombre del producto
    - descripcion_producto: Descripción
    - categoria_producto: Categoría
    - marca_producto: Marca
    """
    try:
        producto_service = ProductoService(session)
        producto_actualizado = producto_service.actualizar_producto(
            producto_id=producto_id,
            producto_update=producto_update
        )
        return {
            "mensaje": "Producto actualizado exitosamente",
            "producto": producto_actualizado
        }
    except ValueError as e:
        raise ValueError(str(e))


@router.patch("/productos/{producto_id}/stock")
def update_product_stock(
    producto_id: int,
    nuevo_stock: int = Query(..., ge=0, description="Nuevo stock"),
    user_data: dict = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """
    Actualizar rápidamente el stock de un producto
    """
    try:
        from sqlmodel import select
        from models.producto import Producto
        
        producto = session.exec(
            select(Producto).where(Producto.id_producto == producto_id)
        ).first()
        
        if not producto:
            raise ValueError(f"Producto {producto_id} no encontrado")
        
        stock_anterior = producto.stock_producto
        producto.stock_producto = nuevo_stock
        session.add(producto)
        session.commit()
        session.refresh(producto)
        
        return {
            "mensaje": "Stock actualizado",
            "producto_id": producto_id,
            "stock_anterior": stock_anterior,
            "stock_nuevo": nuevo_stock,
            "producto": producto
        }
    except Exception as e:
        session.rollback()
        raise ValueError(f"Error al actualizar stock: {str(e)}")


@router.patch("/productos/{producto_id}/precio")
def update_product_price(
    producto_id: int,
    nuevo_precio: Decimal = Query(..., gt=0, description="Nuevo precio"),
    user_data: dict = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """
    Actualizar el precio de un producto
    """
    try:
        from sqlmodel import select
        from models.producto import Producto
        
        producto = session.exec(
            select(Producto).where(Producto.id_producto == producto_id)
        ).first()
        
        if not producto:
            raise ValueError(f"Producto {producto_id} no encontrado")
        
        precio_anterior = producto.precio_producto
        producto.precio_producto = nuevo_precio
        session.add(producto)
        session.commit()
        session.refresh(producto)
        
        return {
            "mensaje": "Precio actualizado",
            "producto_id": producto_id,
            "precio_anterior": float(precio_anterior),
            "precio_nuevo": float(nuevo_precio),
            "producto": producto
        }
    except Exception as e:
        session.rollback()
        raise ValueError(f"Error al actualizar precio: {str(e)}")
