"""
Modelo SQLModel: Dirección
Almacena direcciones de usuarios (1:many)
Un usuario puede tener múltiples direcciones
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field


class Direccion(SQLModel, table=True):
    """
    Tabla: direccion
    Normalizado sin multivalores: provincia, cantón, distrito separados
    """
    __tablename__ = "direccion"

    # Campos principales
    id_direccion: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario")

    # Ubicación normalizada (Costa Rica)
    provincia_direccion: str = Field(max_length=50)
    canton_direccion: str = Field(max_length=50)
    distrito_direccion: str = Field(max_length=50)
    direccion_exacta_direccion: str = Field(max_length=255)  # Calle, número, referencias

    es_principal_direccion: bool = Field(default=False)

    # Timestamps
    fecha_registro_direccion: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuario: "Usuario" = Relationship(back_populates="direcciones")
    pedidos: List["Pedido"] = Relationship(back_populates="direccion_entrega")
    envios: List["Envio"] = Relationship(back_populates="direccion_envio")

    class Config:
        arbitrary_types_allowed = True


# Import al final para evitar circular imports
from models.usuario import Usuario
from models.pedido import Pedido
from models.envio import Envio

