"""
Modelo SQLModel: Usuario
Representación en BD de un cliente/usuario de la tienda
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List


class Usuario(SQLModel, table=True):
    """
    Tabla: usuario
    Almacena información de clientes/usuarios registrados
    """
    __tablename__ = "usuario"

    # Campos principales
    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    nombre_usuario: str = Field(max_length=100, index=True)
    email_usuario: str = Field(max_length=255, unique=True, index=True)
    password_usuario: str = Field(max_length=255)  # Hasheado con bcrypt
    estado_usuario: str = Field(default="activo", max_length=20)  # activo, inactivo
    rol_usuario: str = Field(default="cliente", max_length=20)  # cliente, admin

    # Timestamps
    fecha_registro_usuario: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizado_usuario: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones (reverse)
    direcciones: List["Direccion"] = Relationship(back_populates="usuario")
    pedidos: List["Pedido"] = Relationship(back_populates="usuario")
    reseñas: List["Reseña"] = Relationship(back_populates="usuario")
    lista_deseos: List["ListaDeseos"] = Relationship(back_populates="usuario")

    class Config:
        arbitrary_types_allowed = True

