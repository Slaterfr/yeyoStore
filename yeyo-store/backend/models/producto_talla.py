"""
Modelo SQLModel: ProductoTalla
Tabla de unión many-to-many entre Producto y Talla
Normaliza el problema de multivalores en tallas
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from sqlmodel import Field, UniqueConstraint


class ProductoTalla(SQLModel, table=True):
    """
    Tabla: producto_talla
    Unión many-to-many: cada producto puede tener múltiples tallas
    Cada talla disponible para múltiples productos
    
    Constraint único: (id_producto, id_talla) - solo una vez por combinación
    """
    __tablename__ = "producto_talla"
    __table_args__ = (
        UniqueConstraint("id_producto", "id_talla", name="uk_producto_talla"),
    )

    id_producto_talla: Optional[int] = Field(default=None, primary_key=True)
    id_producto: int = Field(foreign_key="producto.id_producto")
    id_talla: int = Field(foreign_key="talla.id_talla")
    stock_disponible_producto_talla: int = Field(default=0)

    # Relaciones
    producto: "Producto" = Relationship(back_populates="producto_talla")
    talla: "Talla" = Relationship(back_populates="producto_talla")

    class Config:
        arbitrary_types_allowed = True


# Imports al final
from models.producto import Producto
from models.talla import Talla

