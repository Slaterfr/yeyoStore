"""
Schemas Pydantic: Dirección
Validación de direcciones de usuarios
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DireccionCreate(BaseModel):
    """Schema para crear una nueva dirección"""
    provincia_direccion: str = Field(..., min_length=2, max_length=50)
    canton_direccion: str = Field(..., min_length=2, max_length=50)
    distrito_direccion: str = Field(..., min_length=2, max_length=50)
    direccion_exacta_direccion: str = Field(..., min_length=5, max_length=255)
    es_principal_direccion: bool = Field(default=False)


class DireccionUpdate(BaseModel):
    """Schema para actualizar una dirección"""
    provincia_direccion: Optional[str] = Field(None, min_length=2, max_length=50)
    canton_direccion: Optional[str] = Field(None, min_length=2, max_length=50)
    distrito_direccion: Optional[str] = Field(None, min_length=2, max_length=50)
    direccion_exacta_direccion: Optional[str] = Field(None, min_length=5, max_length=255)
    es_principal_direccion: Optional[bool] = None


class DireccionResponse(BaseModel):
    """Schema de respuesta para dirección"""
    id_direccion: int
    id_usuario: int
    provincia_direccion: str
    canton_direccion: str
    distrito_direccion: str
    direccion_exacta_direccion: str
    es_principal_direccion: bool
    fecha_registro_direccion: datetime

    class Config:
        from_attributes = True
