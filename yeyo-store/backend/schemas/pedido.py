"""
Schemas Pydantic: Pedido
Validación de órdenes de compra
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class DetallePedidoCreate(BaseModel):
    """Schema para crear un item en pedido"""
    id_producto: int
    id_talla: int
    cantidad_detalle_pedido: int = Field(..., ge=1)


class DetallePedidoResponse(BaseModel):
    """Schema de respuesta para item en pedido"""
    id_detalle_pedido: int
    id_pedido: int
    id_producto: int
    id_talla: int
    cantidad_detalle_pedido: int
    precio_unitario_detalle_pedido: Decimal
    impuesto_detalle_pedido: Decimal
    subtotal_detalle_pedido: Decimal

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    """Schema para crear un nuevo pedido"""
    detalles: List[DetallePedidoCreate] = Field(..., min_items=1)
    id_direccion_entrega_pedido: int
    codigo_cupon_aplicado: Optional[str] = None  # Código de cupón


class PedidoResponse(BaseModel):
    """Schema de respuesta para pedido"""
    id_pedido: int
    id_usuario: int
    fecha_pedido_pedido: datetime
    fecha_entrega_pedido: Optional[datetime]
    monto_total_pedido: Decimal
    estado_pedido_pedido: str
    detalles: List[DetallePedidoResponse] = []

    class Config:
        from_attributes = True


class PedidoResponseDetallado(PedidoResponse):
    """Schema detallado con información de pago y envío"""
    id_cupon_aplicado_pedido: Optional[int] = None

    class Config:
        from_attributes = True
