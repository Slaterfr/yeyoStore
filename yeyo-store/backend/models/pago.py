"""
Modelo SQLModel: Pago
Información de pago por pedido (1:1)
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlmodel import Field


class Pago(SQLModel, table=True):
    """
    Tabla: pago
    Almacena información de pago por pedido
    Relación 1:1 con Pedido
    """
    __tablename__ = "pago"

    id_pago: Optional[int] = Field(default=None, primary_key=True)
    id_pedido: int = Field(foreign_key="pedido.id_pedido", unique=True)  # 1:1
    metodo_pago_pago: str = Field(max_length=30)  # tarjeta, transferencia, sinpe
    estado_pago_pago: str = Field(default="pendiente", max_length=20)  # pendiente, completado, fallido
    fecha_pago_pago: Optional[datetime] = None

    # Relaciones
    pedido: "Pedido" = Relationship(back_populates="pago")

    class Config:
        arbitrary_types_allowed = True


# Import al final
from models.pedido import Pedido

