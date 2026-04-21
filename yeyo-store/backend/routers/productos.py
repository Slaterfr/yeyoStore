"""
Rutas de productos
"""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from decimal import Decimal

from dependencies.exceptions import ProductoNoEncontrado
from schemas.producto import ProductoResponse, ProductoCreate, ProductoUpdate
from services.producto_service import ProductoService
from db.connection import get_session

router = APIRouter(prefix="/api/productos", tags=["productos"])


@router.get("", response_model=list[ProductoResponse])
def get_all_products(
    q: Optional[str] = Query(None, description="Término de búsqueda"),
    categoria: Optional[str] = Query(None, description="Filtro por categoría"),
    precio_min: Optional[float] = Query(None, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, description="Precio máximo"),
    talla: Optional[str] = Query(None, description="Filtro por talla"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """
    Obtener productos con búsqueda y filtros avanzados
    - q: término de búsqueda en nombre o descripción
    - categoria: filtrar por categoría (Tenis, Casual, Deportivo)
    - precio_min: precio mínimo
    - precio_max: precio máximo
    - talla: filtrar por talla (36-45)
    - skip: Número de productos a saltar (default 0)
    - limit: Número máximo de productos (default 10, máximo 100)
    """
    try:
        producto_service = ProductoService(session)
        
        # Si hay filtros, usar búsqueda avanzada
        if q or categoria or precio_min is not None or precio_max is not None or talla:
            productos = producto_service.buscar_productos_avanzado(
                q=q,
                categoria=categoria,
                precio_min=precio_min,
                precio_max=precio_max,
                talla=talla,
                skip=skip,
                limit=limit,
            )
        else:
            # Si no hay filtros, usar listado simple
            productos = producto_service.obtener_todos_productos(
                skip=skip,
                limit=limit,
            )
        
        return productos
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.get("/categoria/{categoria}", response_model=list[ProductoResponse])
def get_products_by_category(
    categoria: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """
    Obtener productos por categoría
    """
    try:
        producto_service = ProductoService(session)
        productos = producto_service.obtener_productos_por_categoria(
            categoria=categoria,
            skip=skip,
            limit=limit,
        )
        return productos
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.get("/{producto_id}", response_model=ProductoResponse)
def get_product(
    producto_id: int,
    session: Session = Depends(get_session),
):
    """
    Obtener un producto específico con todos sus detalles
    - producto_id: ID del producto
    """
    try:
        producto_service = ProductoService(session)
        producto = producto_service.obtener_producto(producto_id)
        return producto
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.post("", response_model=ProductoResponse, status_code=201)
def create_product(
    producto_create: ProductoCreate,
    session: Session = Depends(get_session),
):
    """
    Crear un nuevo producto (Admin only)
    """
    try:
        producto_service = ProductoService(session)
        producto = producto_service.crear_producto(producto_create)
        return producto
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.put("/{producto_id}", response_model=ProductoResponse)
def update_product(
    producto_id: int,
    producto_update: ProductoUpdate,
    session: Session = Depends(get_session),
):
    """
    Actualizar un producto (Admin only)
    """
    try:
        producto_service = ProductoService(session)
        producto = producto_service.actualizar_producto(
            producto_id=producto_id,
            producto_update=producto_update,
        )
        return producto
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))


@router.get("/{producto_id}/fotos")
def get_product_photos(
    producto_id: int,
    session: Session = Depends(get_session),
):
    """
    Obtener galería de fotos de un producto
    """
    try:
        producto_service = ProductoService(session)
        fotos = producto_service.obtener_fotos_producto(producto_id)
        return {"producto_id": producto_id, "fotos": fotos}
    except ValueError as e:
        raise ProductoNoEncontrado(detail=str(e))

