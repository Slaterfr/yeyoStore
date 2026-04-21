"""
Schemas Pydantic: Producto
Validación de productos y catálogo
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class ProductoCreate(BaseModel):
    """Schema para crear un nuevo producto (admin)"""
    nombre_producto: str = Field(..., min_length=3, max_length=150)
    descripcion_producto: str = Field(default="")
    precio_producto: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    categoria_producto: str = Field(..., min_length=2, max_length=50)
    stock_producto: int = Field(..., ge=0)
    marca_producto: str = Field(..., min_length=2, max_length=50)


class ProductoUpdate(BaseModel):
    """Schema para actualizar un producto"""
    nombre_producto: Optional[str] = Field(None, min_length=3, max_length=150)
    descripcion_producto: Optional[str] = None
    precio_producto: Optional[Decimal] = Field(None, gt=0)
    categoria_producto: Optional[str] = Field(None, min_length=2, max_length=50)
    stock_producto: Optional[int] = Field(None, ge=0)
    marca_producto: Optional[str] = Field(None, min_length=2, max_length=50)


class ProductoResponse(BaseModel):
    """Schema básico de respuesta para producto"""
    id_producto: int
    nombre_producto: str
    descripcion_producto: str
    precio_producto: Decimal
    categoria_producto: str
    stock_producto: int
    marca_producto: str
    promedio_calificacion_producto: float
    fecha_creacion_producto: datetime

    class Config:
        from_attributes = True


class ProductoResponseDetallado(ProductoResponse):
    """Schema detallado con galería y reseñas (futuro)"""
    pass

    class Config:
        from_attributes = True
