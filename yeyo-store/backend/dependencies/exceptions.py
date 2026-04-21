"""
Excepciones personalizadas centralizadas
Utilizadas en servicios y routers
"""
from fastapi import HTTPException, status


class UsuarioNoEncontrado(HTTPException):
    """Usuario no existe en la BD"""
    def __init__(self, detail: str = "Usuario no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class UsuarioYaExiste(HTTPException):
    """Email ya está registrado"""
    def __init__(self, detail: str = "El email ya está registrado"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class CredencialesInvalidas(HTTPException):
    """Email o contraseña incorrectos"""
    def __init__(self, detail: str = "Email o contraseña incorrectos"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenInvalido(HTTPException):
    """JWT token inválido o expirado"""
    def __init__(self, detail: str = "Token inválido o expirado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class NoAutorizado(HTTPException):
    """Usuario no autorizado para esta acción"""
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ProductoNoEncontrado(HTTPException):
    """Producto no existe"""
    def __init__(self, detail: str = "Producto no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class StockInsuficiente(HTTPException):
    """No hay stock suficiente del producto"""
    def __init__(self, detail: str = "Stock insuficiente"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class CuponInvalido(HTTPException):
    """Cupón no existe o inválido"""
    def __init__(self, detail: str = "Cupón inválido"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class CuponExpirado(HTTPException):
    """Cupón ha expirado"""
    def __init__(self, detail: str = "Cupón expirado"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class CuponAgotado(HTTPException):
    """Se alcanzó el límite de usos del cupón"""
    def __init__(self, detail: str = "Cupón agotado - límite de usos alcanzado"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class PedidoNoEncontrado(HTTPException):
    """Pedido no existe"""
    def __init__(self, detail: str = "Pedido no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ReseñaYaExiste(HTTPException):
    """Usuario ya ha reseñado este producto"""
    def __init__(self, detail: str = "Ya has reseñado este producto"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class ErrorValidacion(HTTPException):
    """Error en validación de datos"""
    def __init__(self, detail: str = "Error en validación de datos"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
