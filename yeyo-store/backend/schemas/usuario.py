"""
Schemas Pydantic: Usuario
Validación de entrada y salida para endpoints de usuarios
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UsuarioCreate(BaseModel):
    """Schema para crear un nuevo usuario (registrarse)"""
    nombre_usuario: str = Field(..., min_length=2, max_length=100)
    email_usuario: EmailStr
    password_usuario: str = Field(..., min_length=8, max_length=100)


class UsuarioUpdate(BaseModel):
    """Schema para actualizar datos del usuario"""
    nombre_usuario: Optional[str] = Field(None, min_length=2, max_length=100)
    email_usuario: Optional[EmailStr] = None


class UsuarioResponse(BaseModel):
    """Schema de respuesta para usuario (sin contraseña)"""
    id_usuario: int
    nombre_usuario: str
    email_usuario: str
    estado_usuario: str
    rol_usuario: str
    fecha_registro_usuario: datetime

    class Config:
        from_attributes = True


class UsuarioResponseDetallado(UsuarioResponse):
    """Schema detallado con timestamps"""
    fecha_actualizado_usuario: datetime

    class Config:
        from_attributes = True


class UsuarioResponseConRol(BaseModel):
    """Schema de respuesta con rol incluido"""
    id_usuario: int
    nombre_usuario: str
    email_usuario: str
    rol_usuario: str

    class Config:
        from_attributes = True
