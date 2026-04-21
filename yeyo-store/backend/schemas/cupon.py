"""
Schemas Pydantic: Cupón
Validación de cupones y descuentos
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class CuponCreate(BaseModel):
    """Schema para crear un nuevo cupón (admin)"""
    codigo_cupon: str = Field(..., min_length=3, max_length=20)
    descuento_porcentaje_cupon: Decimal = Field(..., gt=0, le=100)
    maximo_usos_cupon: int = Field(default=0, ge=0)  # 0 = ilimitado
    fecha_expiracion_cupon: Optional[date] = None


class CuponValidate(BaseModel):
    """Schema para validar un cupón"""
    codigo_cupon: str


class CuponResponse(BaseModel):
    """Schema de respuesta para cupón"""
    id_cupon: int
    codigo_cupon: str
    descuento_porcentaje_cupon: Decimal
    maximo_usos_cupon: int
    contador_usos_cupon: int
    fecha_expiracion_cupon: Optional[date]
    esta_activo_cupon: bool
    fecha_creacion_cupon: datetime

    class Config:
        from_attributes = True


class CuponValidateResponse(BaseModel):
    """Respuesta cuando se valida un cupón"""
    es_valido: bool
    mensaje: str
    descuento_porcentaje: Optional[Decimal] = None
    codigo: Optional[str] = None
