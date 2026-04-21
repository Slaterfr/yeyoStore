"""
Modelo SQLModel: Cupón
Sistema de descuentos y promociones
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal


class Cupon(SQLModel, table=True):
    """
    Tabla: cupon
    Almacena cupones/códigos de descuento
    Configurable: descuento%, máximo de usos, fecha de expiración
    """
    __tablename__ = "cupon"

    id_cupon: Optional[int] = Field(default=None, primary_key=True)
    codigo_cupon: str = Field(max_length=20, unique=True, index=True)
    descuento_porcentaje_cupon: Decimal = Field(max_digits=5, decimal_places=2)  # ej: 15.50%
    maximo_usos_cupon: int = Field(ge=0)  # 0 = ilimitado
    contador_usos_cupon: int = Field(default=0)
    fecha_expiracion_cupon: Optional[date] = None  # None = sin expiración
    esta_activo_cupon: bool = Field(default=True)
    fecha_creacion_cupon: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    pedidos: List["Pedido"] = Relationship(back_populates="cupon_aplicado")

    class Config:
        arbitrary_types_allowed = True


# Import al final
from models.pedido import Pedido

