"""
ListaDeseosService
Servicio de gestión de lista de deseos/wishlist
"""
from sqlmodel import Session, select
from models.lista_deseos import ListaDeseos
from models.usuario import Usuario
from models.producto import Producto
from dependencies.exceptions import UsuarioNoEncontrado, ProductoNoEncontrado, ErrorValidacion
from typing import List


class ListaDeseosService:
    """Servicio de gestión de lista de deseos"""

    def __init__(self, session: Session):
        self.session = session

    def obtener_item_wishlist(self, lista_deseos_id: int) -> ListaDeseos:
        """Obtiene un item específico de la wishlist"""
        item = self.session.get(ListaDeseos, lista_deseos_id)
        if not item:
            raise ErrorValidacion("El item no existe en la lista de deseos")
        return item

    def agregar_a_wishlist(self, user_id: int, producto_id: int) -> ListaDeseos:
        """Agrega un producto a la wishlist del usuario"""
        # Verificar usuario
        usuario = self.session.get(Usuario, user_id)
        if not usuario:
            raise UsuarioNoEncontrado()

        # Verificar producto
        producto = self.session.get(Producto, producto_id)
        if not producto:
            raise ProductoNoEncontrado()

        # Verificar que no exista ya
        statement = select(ListaDeseos).where(
            ListaDeseos.id_usuario == user_id,
            ListaDeseos.id_producto == producto_id,
        )
        existe = self.session.exec(statement).first()

        if existe:
            raise ErrorValidacion("El producto ya está en tu lista de deseos")

        # Crear item
        item_lista = ListaDeseos(
            id_usuario=user_id,
            id_producto=producto_id,
        )

        self.session.add(item_lista)
        self.session.commit()
        self.session.refresh(item_lista)

        return item_lista

    def obtener_wishlist_usuario(self, user_id: int) -> List[ListaDeseos]:
        """Obtiene toda la lista de deseos de un usuario"""
        # Verificar usuario
        usuario = self.session.get(Usuario, user_id)
        if not usuario:
            raise UsuarioNoEncontrado()

        statement = select(ListaDeseos).where(
            ListaDeseos.id_usuario == user_id
        ).order_by(ListaDeseos.fecha_agregado_lista_deseos.desc())

        return self.session.exec(statement).all()

    def remover_de_wishlist(self, user_id: int, producto_id: int) -> bool:
        """Remueve un producto de la wishlist"""
        statement = select(ListaDeseos).where(
            ListaDeseos.id_usuario == user_id,
            ListaDeseos.id_producto == producto_id,
        )
        item = self.session.exec(statement).first()

        if not item:
            raise ErrorValidacion("El producto no está en tu lista de deseos")

        self.session.delete(item)
        self.session.commit()

        return True

    def limpiar_wishlist(self, user_id: int) -> int:
        """Limpia toda la wishlist de un usuario"""
        statement = select(ListaDeseos).where(ListaDeseos.id_usuario == user_id)
        items = self.session.exec(statement).all()

        count = len(items)
        for item in items:
            self.session.delete(item)

        self.session.commit()

        return count

