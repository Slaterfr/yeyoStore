"""
Schemas Pydantic - Validación de entrada/salida
Exportación centralizada de todos los schemas
"""

from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioResponseDetallado
from schemas.direccion import DireccionCreate, DireccionUpdate, DireccionResponse
from schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse, ProductoResponseDetallado
from schemas.reseña import ReseñaCreate, ReseñaUpdate, ReseñaResponse
from schemas.lista_deseos import ListaDeseosCreate, ListaDeseosResponse
from schemas.cupon import CuponCreate, CuponValidate, CuponResponse, CuponValidateResponse
from schemas.pedido import DetallePedidoCreate, DetallePedidoResponse, PedidoCreate, PedidoResponse, PedidoResponseDetallado
from schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest

__all__ = [
    # Usuario
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuarioResponseDetallado",
    # Dirección
    "DireccionCreate",
    "DireccionUpdate",
    "DireccionResponse",
    # Producto
    "ProductoCreate",
    "ProductoUpdate",
    "ProductoResponse",
    "ProductoResponseDetallado",
    # Reseña
    "ReseñaCreate",
    "ReseñaUpdate",
    "ReseñaResponse",
    # Lista de Deseos
    "ListaDeseosCreate",
    "ListaDeseosResponse",
    # Cupón
    "CuponCreate",
    "CuponValidate",
    "CuponResponse",
    "CuponValidateResponse",
    # Pedido
    "DetallePedidoCreate",
    "DetallePedidoResponse",
    "PedidoCreate",
    "PedidoResponse",
    "PedidoResponseDetallado",
    # Auth
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
]
