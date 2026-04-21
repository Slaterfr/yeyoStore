"""
Modelo SQLModel: ListaDeseos / Wishlist
Productos favoritos de cada usuario
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlmodel import Field, UniqueConstraint


class ListaDeseos(SQLModel, table=True):
    """
    Tabla: lista_deseos
    Wishlist de cada usuario
    Constraint único: (id_usuario, id_producto) - no duplicados
    """
    __tablename__ = "lista_deseos"
    __table_args__ = (
        UniqueConstraint("id_usuario", "id_producto", name="uk_usuario_producto_lista"),
    )

    id_lista_deseos: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario")
    id_producto: int = Field(foreign_key="producto.id_producto")
    fecha_agregado_lista_deseos: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuario: "Usuario" = Relationship(back_populates="lista_deseos")
    producto: "Producto" = Relationship(back_populates="lista_deseos")

    class Config:
        arbitrary_types_allowed = True


# Imports al final
from models.usuario import Usuario
from models.producto import Producto

