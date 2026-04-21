"""
Modelo SQLModel: DetallePedido
Ítems individuales dentro de cada pedido
Almacena precio al momento de compra (historial)
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from decimal import Decimal
from sqlmodel import Field


class DetallePedido(SQLModel, table=True):
    """
    Tabla: detalle_pedido
    Items individuales de una orden
    Almacena el precio_unitario al momento de compra (para historial)
    Incluye: impuesto (13% IVA, Costa Rica)
    """
    __tablename__ = "detalle_pedido"

    id_detalle_pedido: Optional[int] = Field(default=None, primary_key=True)
    id_pedido: int = Field(foreign_key="pedido.id_pedido")
    id_producto: int = Field(foreign_key="producto.id_producto")
    id_talla: int = Field(foreign_key="talla.id_talla")

    cantidad_detalle_pedido: int = Field(ge=1)
    precio_unitario_detalle_pedido: Decimal = Field(max_digits=10, decimal_places=2)  # NUEVO
    impuesto_detalle_pedido: Decimal = Field(max_digits=10, decimal_places=2)  # 13% IVA
    subtotal_detalle_pedido: Decimal = Field(max_digits=10, decimal_places=2)  # cantidad × precio

    # Relaciones
    pedido: "Pedido" = Relationship(back_populates="detalles")
    producto: "Producto" = Relationship(back_populates="detalles_pedido")
    talla: "Talla" = Relationship()

    class Config:
        arbitrary_types_allowed = True


# Imports al final
from models.pedido import Pedido
from models.producto import Producto
from models.talla import Talla

