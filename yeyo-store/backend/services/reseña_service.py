"""
ReseñaService
Servicio de gestión de reseñas y calificaciones
"""
from sqlmodel import Session, select
from models.reseña import Reseña
from models.usuario import Usuario
from models.producto import Producto
from schemas.reseña import ReseñaCreate, ReseñaUpdate
from dependencies.exceptions import ReseñaYaExiste, ProductoNoEncontrado, UsuarioNoEncontrado, ErrorValidacion
from typing import List
from services.producto_service import ProductoService


class ReseñaService:
    """Servicio de gestión de reseñas"""

    def __init__(self, session: Session):
        self.session = session
        self.producto_service = ProductoService(session)

    def crear_reseña(self, user_id: int, producto_id: int, reseña_create: ReseñaCreate) -> Reseña:
        """
        Crea una nueva reseña
        Validaciones:
        - Usuario existe
        - Producto existe
        - Usuario no ha reseñado este producto antes
        """
        # Verificar usuario
        usuario = self.session.get(Usuario, user_id)
        if not usuario:
            raise UsuarioNoEncontrado()

        # Verificar producto
        producto = self.producto_service.obtener_producto(producto_id)

        # Verificar que no exista reseña anterior
        statement = select(Reseña).where(
            Reseña.id_usuario == user_id,
            Reseña.id_producto == producto_id,
        )
        reseña_existente = self.session.exec(statement).first()

        if reseña_existente:
            raise ReseñaYaExiste()

        # Crear reseña
        nueva_reseña = Reseña(
            id_usuario=user_id,
            id_producto=producto_id,
            calificacion_reseña=reseña_create.calificacion_reseña,
            titulo_reseña=reseña_create.titulo_reseña,
            comentario_reseña=reseña_create.comentario_reseña,
        )

        self.session.add(nueva_reseña)
        self.session.commit()
        self.session.refresh(nueva_reseña)

        # Recalcular rating promedio del producto
        self.producto_service.actualizar_rating_promedio(producto_id)

        return nueva_reseña

    def obtener_reseñas_producto(self, producto_id: int) -> List[Reseña]:
        """Obtiene todas las reseñas de un producto"""
        # Verificar que producto existe
        self.producto_service.obtener_producto(producto_id)

        statement = select(Reseña).where(
            Reseña.id_producto == producto_id
        ).order_by(Reseña.fecha_creacion_reseña.desc())

        return self.session.exec(statement).all()

    def obtener_reseña(self, reseña_id: int) -> Reseña:
        """Obtiene una reseña por ID"""
        reseña = self.session.get(Reseña, reseña_id)

        if not reseña:
            raise ErrorValidacion("Reseña no encontrada")

        return reseña

    def actualizar_reseña(self, reseña_id: int, user_id: int, reseña_update: ReseñaUpdate) -> Reseña:
        """Actualiza una reseña (solo si es del usuario)"""
        reseña = self.obtener_reseña(reseña_id)

        if reseña.id_usuario != user_id:
            raise ErrorValidacion("No puedes editar una reseña que no es tuya")

        if reseña_update.calificacion_reseña:
            reseña.calificacion_reseña = reseña_update.calificacion_reseña

        if reseña_update.titulo_reseña:
            reseña.titulo_reseña = reseña_update.titulo_reseña

        if reseña_update.comentario_reseña is not None:
            reseña.comentario_reseña = reseña_update.comentario_reseña

        self.session.add(reseña)
        self.session.commit()
        self.session.refresh(reseña)

        # Recalcular rating
        self.producto_service.actualizar_rating_promedio(reseña.id_producto)

        return reseña

    def eliminar_reseña(self, reseña_id: int, user_id: int) -> bool:
        """Elimina una reseña (solo si es del usuario)"""
        reseña = self.obtener_reseña(reseña_id)

        if reseña.id_usuario != user_id:
            raise ErrorValidacion("No puedes eliminar una reseña que no es tuya")

        producto_id = reseña.id_producto
        self.session.delete(reseña)
        self.session.commit()

        # Recalcular rating
        self.producto_service.actualizar_rating_promedio(producto_id)

        return True

