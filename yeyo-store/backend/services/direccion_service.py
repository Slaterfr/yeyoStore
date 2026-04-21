"""
DireccionService
Servicio para gestión de direcciones
"""
from sqlmodel import Session, select
from models.direccion import Direccion
from models.usuario import Usuario
from schemas.direccion import DireccionCreate, DireccionUpdate
from dependencies.exceptions import UsuarioNoEncontrado, ErrorValidacion
from typing import List


class DireccionService:
    """Servicio de gestión de direcciones"""

    def __init__(self, session: Session):
        self.session = session

    def crear_direccion(self, user_id: int, direccion_create: DireccionCreate) -> Direccion:
        """Crea una nueva dirección para un usuario"""
        # Verificar que el usuario existe
        usuario = self.session.get(Usuario, user_id)
        if not usuario:
            raise UsuarioNoEncontrado()

        # Si es principal, desmarcar otras direcciones
        if direccion_create.es_principal_direccion:
            statement = select(Direccion).where(
                Direccion.id_usuario == user_id,
                Direccion.es_principal_direccion == True,
            )
            direcciones_principales = self.session.exec(statement).all()
            for dir in direcciones_principales:
                dir.es_principal_direccion = False
                self.session.add(dir)

        nueva_direccion = Direccion(
            id_usuario=user_id,
            provincia_direccion=direccion_create.provincia_direccion,
            canton_direccion=direccion_create.canton_direccion,
            distrito_direccion=direccion_create.distrito_direccion,
            direccion_exacta_direccion=direccion_create.direccion_exacta_direccion,
            es_principal_direccion=direccion_create.es_principal_direccion,
        )

        self.session.add(nueva_direccion)
        self.session.commit()
        self.session.refresh(nueva_direccion)

        return nueva_direccion

    def obtener_direcciones_usuario(self, user_id: int) -> List[Direccion]:
        """Obtiene todas las direcciones de un usuario"""
        statement = select(Direccion).where(Direccion.id_usuario == user_id)
        return self.session.exec(statement).all()

    def obtener_direccion(self, direccion_id: int, user_id: int) -> Direccion:
        """Obtiene una dirección específica (asegura que pertenezca al usuario)"""
        statement = select(Direccion).where(
            Direccion.id_direccion == direccion_id,
            Direccion.id_usuario == user_id,
        )
        direccion = self.session.exec(statement).first()

        if not direccion:
            raise ErrorValidacion("Dirección no encontrada")

        return direccion

    def actualizar_direccion(
        self, direccion_id: int, user_id: int, direccion_update: DireccionUpdate
    ) -> Direccion:
        """Actualiza una dirección"""
        direccion = self.obtener_direccion(direccion_id, user_id)

        if direccion_update.provincia_direccion:
            direccion.provincia_direccion = direccion_update.provincia_direccion

        if direccion_update.canton_direccion:
            direccion.canton_direccion = direccion_update.canton_direccion

        if direccion_update.distrito_direccion:
            direccion.distrito_direccion = direccion_update.distrito_direccion

        if direccion_update.direccion_exacta_direccion:
            direccion.direccion_exacta_direccion = direccion_update.direccion_exacta_direccion

        if direccion_update.es_principal_direccion is not None:
            direccion.es_principal_direccion = direccion_update.es_principal_direccion

        self.session.add(direccion)
        self.session.commit()
        self.session.refresh(direccion)

        return direccion

    def eliminar_direccion(self, direccion_id: int, user_id: int) -> bool:
        """Elimina una dirección"""
        direccion = self.obtener_direccion(direccion_id, user_id)
        self.session.delete(direccion)
        self.session.commit()
        return True

