"""
Modelo SQLModel: Pedido
Órdenes/compras realizadas por usuarios
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from sqlmodel import Field


class Pedido(SQLModel, table=True):
    """
    Tabla: pedido
    Almacena órdenes de compra
    Relaciones: Usuario (many:1), Dirección (many:1), Cupón (many:1), DetallePedido (1:many)
    """
    __tablename__ = "pedido"

    id_pedido: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario")
    id_direccion_entrega_pedido: int = Field(foreign_key="direccion.id_direccion")
    id_cupon_aplicado_pedido: Optional[int] = Field(default=None, foreign_key="cupon.id_cupon")

    fecha_pedido_pedido: datetime = Field(default_factory=datetime.utcnow)
    fecha_entrega_pedido: Optional[datetime] = None
    monto_total_pedido: Decimal = Field(max_digits=12, decimal_places=2)  # Total con descuento
    estado_pedido_pedido: str = Field(default="pendiente", max_length=20)  # pendiente, confirmado, enviado, entregado
    fecha_creacion_pedido: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuario: "Usuario" = Relationship(back_populates="pedidos")
    direccion_entrega: "Direccion" = Relationship(back_populates="pedidos")
    cupon_aplicado: Optional["Cupon"] = Relationship(back_populates="pedidos")
    detalles: List["DetallePedido"] = Relationship(back_populates="pedido")
    pago: Optional["Pago"] = Relationship(back_populates="pedido")
    envio: Optional["Envio"] = Relationship(back_populates="pedido")

    class Config:
        arbitrary_types_allowed = True


# Imports al final para evitar circular imports
from models.usuario import Usuario
from models.direccion import Direccion
from models.cupon import Cupon
from models.detalle_pedido import DetallePedido
from models.pago import Pago
from models.envio import Envio

