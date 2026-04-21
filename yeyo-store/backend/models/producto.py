"""
Modelo SQLModel: Producto
Catálogo de productos/zapatos disponibles en la tienda
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class Producto(SQLModel, table=True):
    """
    Tabla: producto
    Almacena información de zapatos disponibles en la tienda
    """
    __tablename__ = "producto"

    id_producto: Optional[int] = Field(default=None, primary_key=True)
    nombre_producto: str = Field(max_length=150, index=True)
    descripcion_producto: str = Field(default="")  # TEXT - puede ser muy largo
    precio_producto: Decimal = Field(max_digits=10, decimal_places=2)  # NUMERIC(10,2)
    categoria_producto: str = Field(max_length=50, index=True)  # tenis, casual, deportivo
    stock_producto: int = Field(default=0)
    marca_producto: str = Field(max_length=50)

    # Calificación promedio calculada
    promedio_calificacion_producto: float = Field(default=0.0)

    fecha_creacion_producto: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    fotos: List["FotoProducto"] = Relationship(back_populates="producto")
    reseñas: List["Reseña"] = Relationship(back_populates="producto")
    detalles_pedido: List["DetallePedido"] = Relationship(back_populates="producto")
    lista_deseos: List["ListaDeseos"] = Relationship(back_populates="producto")
    producto_talla: List["ProductoTalla"] = Relationship(back_populates="producto")

    class Config:
        arbitrary_types_allowed = True


# Imports al final
from models.foto_producto import FotoProducto
from models.reseña import Reseña
from models.detalle_pedido import DetallePedido
from models.lista_deseos import ListaDeseos
from models.producto_talla import ProductoTalla

