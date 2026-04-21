"""
Modelo SQLModel: FotoProducto
Galería de imágenes para cada producto
Soporta URLs externas (Cloudinary, etc)
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlmodel import Field


class FotoProducto(SQLModel, table=True):
    """
    Tabla: foto_producto
    Galería de fotos por producto
    Soporta múltiples imágenes, orden y principal
    """
    __tablename__ = "foto_producto"

    id_foto_producto: Optional[int] = Field(default=None, primary_key=True)
    id_producto: int = Field(foreign_key="producto.id_producto")
    url_foto_producto: str = Field(max_length=500)  # URL externa
    es_principal_foto_producto: bool = Field(default=False)
    orden_foto_producto: int = Field(default=0)  # Para ordenar en galería
    fecha_subida_foto_producto: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    producto: "Producto" = Relationship(back_populates="fotos")

    class Config:
        arbitrary_types_allowed = True


# Import al final
from models.producto import Producto

