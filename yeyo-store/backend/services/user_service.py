"""
UserService
Servicio de gestión de usuarios
"""
from sqlmodel import Session, select
from models.usuario import Usuario
from schemas.usuario import UsuarioUpdate, UsuarioResponse
from dependencies.exceptions import UsuarioNoEncontrado, ErrorValidacion


class UserService:
    """Servicio para operaciones con usuarios"""

    def __init__(self, session: Session):
        self.session = session

    def obtener_usuario(self, user_id: int) -> Usuario:
        """Obtiene un usuario por ID"""
        statement = select(Usuario).where(Usuario.id_usuario == user_id)
        usuario = self.session.exec(statement).first()

        if not usuario:
            raise UsuarioNoEncontrado()

        return usuario

    def actualizar_usuario(self, user_id: int, usuario_update: UsuarioUpdate) -> Usuario:
        """Actualiza datos del usuario"""
        usuario = self.obtener_usuario(user_id)

        if usuario_update.nombre_usuario:
            usuario.nombre_usuario = usuario_update.nombre_usuario

        if usuario_update.email_usuario:
            # Verificar que el nuevo email no exista
            statement = select(Usuario).where(
                Usuario.email_usuario == usuario_update.email_usuario,
                Usuario.id_usuario != user_id,
            )
            if self.session.exec(statement).first():
                raise ErrorValidacion("Email ya está en uso")

            usuario.email_usuario = usuario_update.email_usuario

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario

    def desactivar_usuario(self, user_id: int) -> Usuario:
        """Desactiva un usuario"""
        usuario = self.obtener_usuario(user_id)
        usuario.estado_usuario = "inactivo"

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario

