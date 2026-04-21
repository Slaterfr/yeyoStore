"""
Rutas de autenticación
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from dependencies.exceptions import (
    CredencialesInvalidas,
    UsuarioYaExiste,
    TokenInvalido,
)
from dependencies.auth import get_current_user_id
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse, RefreshTokenRequest
from schemas.usuario import UsuarioCreate
from services.auth_service import AuthService
from db.connection import get_session

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(
    request: RegisterRequest,
    session: Session = Depends(get_session),
):
    """
    Registrar un nuevo usuario
    - nombre_usuario: Nombre de usuario único
    - email_usuario: Email único
    - password_usuario: Contraseña (será hasheada)
    """
    try:
        auth_service = AuthService(session)
        usuario_create = UsuarioCreate(
            nombre_usuario=request.nombre_usuario,
            email_usuario=request.email_usuario,
            password_usuario=request.password_usuario,
        )
        tokens = auth_service.registrar_usuario(usuario_create)
        return tokens
    except ValueError as e:
        raise UsuarioYaExiste(detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    session: Session = Depends(get_session),
):
    """
    Iniciar sesión y obtener tokens JWT
    - email_usuario: Email del usuario
    - password_usuario: Contraseña
    """
    try:
        auth_service = AuthService(session)
        tokens = auth_service.login(request)
        return tokens
    except ValueError as e:
        raise CredencialesInvalidas(detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshTokenRequest,
    session: Session = Depends(get_session),
):
    """
    Obtener nuevo access token usando refresh token
    - refresh_token: Token de refresco válido
    """
    try:
        auth_service = AuthService(session)
        tokens = auth_service.refresh_token_access(
            refresh_token=request.refresh_token
        )
        return tokens
    except ValueError as e:
        raise TokenInvalido(detail=str(e))


@router.get("/me")
def get_current_user(current_user_id: int = Depends(get_current_user_id)):
    """
    Obtener información del usuario actual (requiere token válido)
    """
    return {"usuario_id": current_user_id, "message": "Token válido"}

