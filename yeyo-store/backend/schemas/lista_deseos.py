"""
Schemas Pydantic: Lista de Deseos / Wishlist
Validación de wishlist
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ListaDeseosCreate(BaseModel):
    """Schema para agregar a wishlist"""
    id_producto: int


class ListaDeseosResponse(BaseModel):
    """Schema de respuesta para item en wishlist"""
    id_lista_deseos: int
    id_usuario: int
    id_producto: int
    fecha_agregado_lista_deseos: datetime

    class Config:
        from_attributes = True
