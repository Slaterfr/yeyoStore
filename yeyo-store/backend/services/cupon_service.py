"""
CuponService
Servicio de gestión de cupones y descuentos
"""
from sqlmodel import Session, select
from models.cupon import Cupon
from dependencies.exceptions import CuponInvalido, CuponExpirado, CuponAgotado, ErrorValidacion
from datetime import date
from typing import Optional
from decimal import Decimal


class CuponService:
    """Servicio de gestión de cupones"""

    def __init__(self, session: Session):
        self.session = session

    def crear_cupon(
        self,
        codigo: str,
        descuento: Decimal,
        maximo_usos: int = 0,
        fecha_expiracion: Optional[date] = None,
    ) -> Cupon:
        """Crea un nuevo cupón (admin)"""
        # Verificar que el código no exista
        statement = select(Cupon).where(Cupon.codigo_cupon == codigo)
        if self.session.exec(statement).first():
            raise ErrorValidacion("El código de cupón ya existe")

        nuevo_cupon = Cupon(
            codigo_cupon=codigo,
            descuento_porcentaje_cupon=descuento,
            maximo_usos_cupon=maximo_usos,
            fecha_expiracion_cupon=fecha_expiracion,
            esta_activo_cupon=True,
            contador_usos_cupon=0,
        )

        self.session.add(nuevo_cupon)
        self.session.commit()
        self.session.refresh(nuevo_cupon)

        return nuevo_cupon

    def validar_cupon(self, codigo: str) -> Cupon:
        """
        Valida un cupón
        
        Comprueba:
        - Código existe
        - Está activo
        - No ha expirado
        - No ha agotado usos
        
        Raises:
            CuponInvalido: Código no existe
            ErrorValidacion: Cupón inactivo
            CuponExpirado: Cupón expirado
            CuponAgotado: Límite de usos alcanzado
        """
        statement = select(Cupon).where(Cupon.codigo_cupon == codigo)
        cupon = self.session.exec(statement).first()

        if not cupon:
            raise CuponInvalido()

        if not cupon.esta_activo_cupon:
            raise ErrorValidacion("Cupón está inactivo")

        if cupon.fecha_expiracion_cupon and cupon.fecha_expiracion_cupon < date.today():
            raise CuponExpired()

        if cupon.maximo_usos_cupon > 0 and cupon.contador_usos_cupon >= cupon.maximo_usos_cupon:
            raise CuponAgotado()

        return cupon

    def aplicar_cupon(self, codigo: str) -> tuple[Cupon, Decimal]:
        """
        Aplica un cupón y retorna el descuento
        
        Returns:
            (cupon, descuento_porcentaje)
        """
        cupon = self.validar_cupon(codigo)

        # Incrementar contador de usos
        cupon.contador_usos_cupon += 1

        # Desactivar si se alcanzó el límite
        if cupon.maximo_usos_cupon > 0 and cupon.contador_usos_cupon >= cupon.maximo_usos_cupon:
            cupon.esta_activo_cupon = False

        self.session.add(cupon)
        self.session.commit()

        return cupon, cupon.descuento_porcentaje_cupon

    def obtener_cupon(self, cupon_id: int) -> Cupon:
        """Obtiene un cupón por ID"""
        cupon = self.session.get(Cupon, cupon_id)

        if not cupon:
            raise ErrorValidacion("Cupón no encontrado")

        return cupon

    def desactivar_cupon(self, cupon_id: int) -> Cupon:
        """Desactiva un cupón"""
        cupon = self.obtener_cupon(cupon_id)
        cupon.esta_activo_cupon = False

        self.session.add(cupon)
        self.session.commit()
        self.session.refresh(cupon)

        return cupon

    def calcular_descuento(self, monto_total: Decimal, descuento_porcentaje: Decimal) -> Decimal:
        """Calcula el monto del descuento"""
        return monto_total * (descuento_porcentaje / Decimal(100))

    def calcular_monto_con_descuento(
        self,
        monto_total: Decimal,
        descuento_porcentaje: Decimal,
    ) -> Decimal:
        """Calcula el monto final con descuento aplicado"""
        descuento = self.calcular_descuento(monto_total, descuento_porcentaje)
        return monto_total - descuento

