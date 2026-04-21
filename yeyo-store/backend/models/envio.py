"""
Modelo SQLModel: Envío
Información de envío por pedido (1:1)
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlmodel import Field


class Envio(SQLModel, table=True):
    """
    Tabla: envio
    Almacena información de envío por pedido
    Relación 1:1 con Pedido, many:1 con Dirección
    """
    __tablename__ = "envio"

    id_envio: Optional[int] = Field(default=None, primary_key=True)
    id_pedido: int = Field(foreign_key="pedido.id_pedido", unique=True)  # 1:1
    id_direccion_envio: int = Field(foreign_key="direccion.id_direccion")
    estado_envio_envio: str = Field(default="pendiente", max_length=20)  # pendiente, en_transito, entregado
    fecha_envio_envio: Optional[datetime] = None
    costo_envio_envio: Decimal = Field(max_digits=8, decimal_places=2)

    # Relaciones
    pedido: "Pedido" = Relationship(back_populates="envio")
    direccion_envio: "Direccion" = Relationship(back_populates="envios")

    class Config:
        arbitrary_types_allowed = True


# Imports al final
from models.pedido import Pedido
from models.direccion import Direccion

