"""
Schemas Pydantic: Talla
"""
from pydantic import BaseModel


class TallaResponse(BaseModel):
    """Schema de respuesta para talla"""
    id_talla: int
    valor_talla: str
    tipo_medida_talla: str

    class Config:
        from_attributes = True
