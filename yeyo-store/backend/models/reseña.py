"""
Modelo SQLModel: Reseña
Comentarios y calificaciones de productos
Un usuario, una reseña por producto
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlmodel import Field, UniqueConstraint


class Reseña(SQLModel, table=True):
    """
    Tabla: reseña
    Almacena reseñas, calificaciones y comentarios de usuarios
    Constraint único: (id_usuario, id_producto) - solo una reseña por usuario/producto
    """
    __tablename__ = "reseña"
    __table_args__ = (
        UniqueConstraint("id_usuario", "id_producto", name="uk_usuario_producto_reseña"),
    )

    id_reseña: Optional[int] = Field(default=None, primary_key=True)
    id_producto: int = Field(foreign_key="producto.id_producto")
    id_usuario: int = Field(foreign_key="usuario.id_usuario")

    calificacion_reseña: int = Field(ge=1, le=5)  # 1-5 stars
    titulo_reseña: str = Field(max_length=100)
    comentario_reseña: str = Field(default="")  # TEXT

    fecha_creacion_reseña: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizado_reseña: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    producto: "Producto" = Relationship(back_populates="reseñas")
    usuario: "Usuario" = Relationship(back_populates="reseñas")

    class Config:
        arbitrary_types_allowed = True


# Imports al final
from models.producto import Producto
from models.usuario import Usuario

