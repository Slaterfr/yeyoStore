"""
AuthService
Servicio de autenticación centralizado
- Hashing de contraseñas
- Generación y validación de JWT tokens
- Lógica de login/register
"""
from sqlmodel import Session, select
from models.usuario import Usuario
from schemas.auth import LoginRequest, TokenResponse
from schemas.usuario import UsuarioCreate
from dependencies.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from dependencies.exceptions import (
    UsuarioNoEncontrado,
    UsuarioYaExiste,
    CredencialesInvalidas,
    TokenInvalido,
)


class AuthService:
    """Servicio de autenticación"""

    def __init__(self, session: Session):
        self.session = session

    def registrar_usuario(self, usuario_create: UsuarioCreate) -> TokenResponse:
        """
        Registra un nuevo usuario y retorna tokens
        
        Args:
            usuario_create: Datos del nuevo usuario
            
        Returns:
            TokenResponse con access_token y refresh_token
            
        Raises:
            UsuarioYaExiste: Si el email ya está registrado
        """
        # Verificar que el email no exista
        statement = select(Usuario).where(
            Usuario.email_usuario == usuario_create.email_usuario
        )
        usuario_existente = self.session.exec(statement).first()
        
        if usuario_existente:
            raise UsuarioYaExiste()

        # Hashear contraseña
        password_hasheada = hash_password(usuario_create.password_usuario)

        # Crear usuario
        nuevo_usuario = Usuario(
            nombre_usuario=usuario_create.nombre_usuario,
            email_usuario=usuario_create.email_usuario,
            password_usuario=password_hasheada,
            estado_usuario="activo",
        )

        self.session.add(nuevo_usuario)
        self.session.commit()
        self.session.refresh(nuevo_usuario)

        # Generar tokens con rol
        access_token = create_access_token({
            "sub": str(nuevo_usuario.id_usuario),
            "rol": nuevo_usuario.rol_usuario
        })
        refresh_token = create_refresh_token(nuevo_usuario.id_usuario)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def login(self, login_request: LoginRequest) -> TokenResponse:
        """
        Autentica un usuario y retorna tokens
        
        Args:
            login_request: Email y contraseña
            
        Returns:
            TokenResponse con access_token y refresh_token
            
        Raises:
            CredencialesInvalidas: Si email o contraseña son incorrectos
        """
        # Buscar usuario por email
        statement = select(Usuario).where(
            Usuario.email_usuario == login_request.email_usuario
        )
        usuario = self.session.exec(statement).first()

        if not usuario:
            raise CredencialesInvalidas()

        # Verificar contraseña
        if not verify_password(login_request.password_usuario, usuario.password_usuario):
            raise CredencialesInvalidas()

        # Generar tokens con rol
        access_token = create_access_token({
            "sub": str(usuario.id_usuario),
            "rol": usuario.rol_usuario
        })
        refresh_token = create_refresh_token(usuario.id_usuario)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh_token_access(self, refresh_token: str) -> TokenResponse:
        """
        Genera un nuevo access token usando refresh token
        
        Args:
            refresh_token: Token de refresco válido
            
        Returns:
            TokenResponse con nuevo access_token
            
        Raises:
            TokenInvalido: Si el refresh token es inválido
        """
        # Validar refresh token
        payload = decode_token(refresh_token)

        token_type = payload.get("type")
        if token_type != "refresh":
            raise TokenInvalido("No es un refresh token válido")

        user_id = payload.get("sub")
        if not user_id:
            raise TokenInvalido()

        # Generar nuevo access token
        access_token = create_access_token({"sub": user_id})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,  # Reutilizamos el mismo refresh token
        )

    def obtener_usuario_por_id(self, user_id: int) -> Usuario:
        """Obtiene un usuario por su ID"""
        statement = select(Usuario).where(Usuario.id_usuario == user_id)
        usuario = self.session.exec(statement).first()

        if not usuario:
            raise UsuarioNoEncontrado()

        return usuario

