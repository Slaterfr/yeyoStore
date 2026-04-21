"""
Modelo SQLModel: Talla
Catálogo de tallas disponibles para zapatos
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Talla(SQLModel, table=True):
    """
    Tabla: talla
    Tallas estándar de zapatos (36-48 EU, 4-14 US, etc)
    """
    __tablename__ = "talla"

    id_talla: Optional[int] = Field(default=None, primary_key=True)
    valor_talla: str = Field(max_length=5, unique=True)  # '36', '37', '38', etc
    tipo_medida_talla: str = Field(max_length=20)  # 'EU', 'US', 'CM'

    # Relaciones
    producto_talla: List["ProductoTalla"] = Relationship(back_populates="talla")

    class Config:
        arbitrary_types_allowed = True


# Import al final
from models.producto_talla import ProductoTalla

