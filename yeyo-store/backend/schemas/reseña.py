"""
Schemas Pydantic: Reseña
Validación de reseñas y calificaciones
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReseñaCreate(BaseModel):
    """Schema para crear una nueva reseña"""
    calificacion_reseña: int = Field(..., ge=1, le=5)
    titulo_reseña: str = Field(..., min_length=3, max_length=100)
    comentario_reseña: str = Field(default="", max_length=1000)


class ReseñaUpdate(BaseModel):
    """Schema para actualizar una reseña"""
    calificacion_reseña: Optional[int] = Field(None, ge=1, le=5)
    titulo_reseña: Optional[str] = Field(None, min_length=3, max_length=100)
    comentario_reseña: Optional[str] = Field(None, max_length=1000)


class ReseñaResponse(BaseModel):
    """Schema de respuesta para reseña"""
    id_reseña: int
    id_producto: int
    id_usuario: int
    calificacion_reseña: int
    titulo_reseña: str
    comentario_reseña: str
    fecha_creacion_reseña: datetime
    fecha_actualizado_reseña: datetime

    class Config:
        from_attributes = True
