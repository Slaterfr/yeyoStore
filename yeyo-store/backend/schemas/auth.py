"""
Schemas Pydantic: Autenticación
Validación de login y tokens
"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Schema para registrarse - requiere nombre de usuario"""
    nombre_usuario: str = Field(..., min_length=2, max_length=100)
    email_usuario: EmailStr
    password_usuario: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    """Schema para login"""
    email_usuario: EmailStr
    password_usuario: str


class TokenResponse(BaseModel):
    """Schema de respuesta con tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Schema para refrescar access token"""
    refresh_token: str
