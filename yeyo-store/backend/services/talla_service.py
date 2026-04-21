"""
Servicio de gestión de tallas
"""
from sqlmodel import Session, select

from models.talla import Talla


class TallaService:
    """Servicio para gestionar tallas"""

    def __init__(self, session: Session):
        self.session = session

    def obtener_todas_las_tallas(self) -> list[Talla]:
        """
        Obtener todas las tallas disponibles
        """
        tallas = self.session.exec(select(Talla).order_by(Talla.valor_talla)).all()
        return tallas

    def obtener_talla_por_valor(self, valor: str) -> Talla | None:
        """
        Obtener talla por su valor (ej: '40')
        """
        talla = self.session.exec(
            select(Talla).where(Talla.valor_talla == valor)
        ).first()
        return talla

    def obtener_talla_por_id(self, id_talla: int) -> Talla | None:
        """
        Obtener talla por su ID
        """
        return self.session.get(Talla, id_talla)
