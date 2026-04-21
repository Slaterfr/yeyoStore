"""
Funciones de autenticación y JWT
Hashing de contraseñas, generación/validación de tokens
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from dependencies.exceptions import TokenInvalido


# Configurar bcrypt para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de seguridad HTTP Bearer
security = HTTPBearer()


# =====================================================================
# FUNCIONES DE HASHING DE CONTRASEÑAS
# =====================================================================

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash bcrypt seguro
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash almacenado en BD
        
    Returns:
        True si coinciden, False caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)


# =====================================================================
# FUNCIONES DE TOKENS JWT
# =====================================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un JWT access token
    
    Args:
        data: Datos a incluir en el token (ej: {"sub": user_id})
        expires_delta: Tiempo de expiración (si None, usa ACCESS_TOKEN_EXPIRE_MINUTES)
        
    Returns:
        JWT token codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un JWT refresh token de larga duración
    
    Args:
        user_id: ID del usuario
        expires_delta: Tiempo de expiración (si None, usa REFRESH_TOKEN_EXPIRE_DAYS)
        
    Returns:
        JWT refresh token codificado
    """
    data = {"sub": str(user_id)}
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    data.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decodifica y valida un JWT token
    
    Args:
        token: JWT token a decodificar
        
    Returns:
        Payload del token decodificado
        
    Raises:
        TokenInvalido: Si el token es inválido o está expirado
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenInvalido("Token expirado")
    except jwt.JWTClaimsError:
        raise TokenInvalido("Token inválido")
    except jwt.DecodeError:
        raise TokenInvalido("No se pudo decodificar el token")


# =====================================================================
# DEPENDENCIES PARA ROUTES
# =====================================================================

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Extrae y valida el user_id del JWT en el header Authorization
    
    Uso en routers:
        @router.get("/me")
        async def get_me(user_id: int = Depends(get_current_user_id)):
            ...
    
    Args:
        credentials: HTTP Bearer token del header
        
    Returns:
        ID del usuario autenticado
        
    Raises:
        TokenInvalido: Si el token es inválido
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise TokenInvalido("Token no contiene user_id")
    
    return int(user_id)


async def get_current_user_with_role(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Extrae user_id y rol del JWT
    
    Uso en routers:
        @router.get("/admin/inventario")
        async def get_inventory(user_data: dict = Depends(get_current_user_with_role)):
            user_id = user_data["user_id"]
            rol = user_data["rol"]
            ...
    
    Args:
        credentials: HTTP Bearer token del header
        
    Returns:
        Dict con keys: user_id, rol
        
    Raises:
        TokenInvalido: Si el token es inválido o no contiene rol
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise TokenInvalido("Token no contiene user_id")
    
    rol: str = payload.get("rol", "cliente")  # Default a cliente si no existe
    
    return {"user_id": int(user_id), "rol": rol}


def require_role(*required_roles):
    """
    Factory para crear un dependency que valida roles
    
    Uso en routers:
        @router.get("/admin/something")
        async def admin_endpoint(user_data: dict = Depends(require_role("admin"))):
            ...
    
    Args:
        required_roles: Roles permitidos (ej: "admin", "cliente")
        
    Returns:
        Dependency que valida el rol
        
    Raises:
        NoAutorizado: Si el usuario no tiene uno de los roles requeridos
    """
    async def check_role(user_data: dict = Depends(get_current_user_with_role)):
        from dependencies.exceptions import NoAutorizado
        
        if user_data["rol"] not in required_roles:
            raise NoAutorizado(
                detail=f"Se requiere uno de estos roles: {', '.join(required_roles)}"
            )
        return user_data
    
    return check_role
