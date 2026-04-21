"""
Servicio de gestión de pedidos
"""
from sqlmodel import Session
from datetime import datetime
from decimal import Decimal

from models.pedido import Pedido
from models.detalle_pedido import DetallePedido
from models.producto import Producto
from models.envio import Envio
from models.pago import Pago
from schemas.pedido import PedidoCreate, DetallePedidoResponse, PedidoResponse
from repositories.base_repository import BaseRepository


class PedidoService:
    """Servicio para gestionar pedidos y órdenes"""

    def __init__(self, session: Session):
        self.session = session
        self.repository = BaseRepository(session, Pedido)

    def crear_pedido(
        self,
        user_id: int,
        pedido_create: PedidoCreate,
        cupon=None,
    ) -> PedidoResponse:
        """
        Crear una nueva orden
        
        Pasos:
        1. Validar que existan los productos
        2. Validar que haya stock suficiente
        3. Calcular monto total
        4. Crear pedido
        5. Crear detalles de pedido
        6. Decrementar stock de productos
        """
        try:
            # Validar productos y calcular monto
            monto_total = Decimal("0")
            detalles_items = []
            
            for detalle in pedido_create.detalles:
                # Obtener producto
                producto = self.session.query(Producto).filter(
                    Producto.id_producto == detalle.id_producto
                ).first()
                
                if not producto:
                    raise ValueError(f"Producto {detalle.id_producto} no encontrado")
                
                # Validar stock
                if producto.stock_producto < detalle.cantidad_detalle_pedido:
                    raise ValueError(
                        f"Stock insuficiente para {producto.nombre_producto}. "
                        f"Disponible: {producto.stock_producto}, Solicitado: {detalle.cantidad_detalle_pedido}"
                    )
                
                # Calcular subtotal usando precio actual del producto
                precio_unitario = Decimal(str(producto.precio_producto))
                subtotal = Decimal(str(detalle.cantidad_detalle_pedido)) * precio_unitario
                monto_total += subtotal
                
                detalles_items.append({
                    "producto": producto,
                    "id_talla": detalle.id_talla,
                    "cantidad": detalle.cantidad_detalle_pedido,
                    "precio_unitario": precio_unitario,
                    "subtotal": subtotal,
                })
            
            # Aplicar descuento del cupón si existe
            monto_descuento = Decimal("0")
            if cupon:
                monto_descuento = (
                    monto_total * Decimal(str(cupon.descuento_porcentaje_cupon)) / 100
                )
            
            monto_final = monto_total - monto_descuento
            
            # Crear pedido
            nuevo_pedido = Pedido(
                id_usuario=user_id,
                id_direccion_entrega_pedido=pedido_create.id_direccion_entrega_pedido,
                id_cupon_aplicado_pedido=cupon.id_cupon if cupon else None,
                monto_total_pedido=monto_final,
                estado_pedido_pedido="pendiente",
                fecha_pedido_pedido=datetime.utcnow(),
            )
            
            self.session.add(nuevo_pedido)
            self.session.flush()  # Para obtener el ID del pedido
            
            # Crear detalles de pedido y decrementar stock
            for detalle in detalles_items:
                # Calcular impuesto (13% IVA)
                impuesto = detalle["subtotal"] * Decimal("0.13")
                
                nuevo_detalle = DetallePedido(
                    id_pedido=nuevo_pedido.id_pedido,
                    id_producto=detalle["producto"].id_producto,
                    id_talla=detalle["id_talla"],
                    cantidad_detalle_pedido=detalle["cantidad"],
                    precio_unitario_detalle_pedido=detalle["precio_unitario"],
                    impuesto_detalle_pedido=impuesto,
                    subtotal_detalle_pedido=detalle["subtotal"],
                )
                
                self.session.add(nuevo_detalle)
                
                # Decrementar stock
                detalle["producto"].stock_producto -= detalle["cantidad"]
            
            # Crear envío
            nuevo_envio = Envio(
                id_pedido=nuevo_pedido.id_pedido,
                id_direccion_envio=pedido_create.id_direccion_entrega_pedido,
                estado_envio_envio="pendiente",
                fecha_envio_envio=datetime.utcnow(),
                costo_envio_envio=Decimal("0"),  # TODO: Calcular costo de envío
            )
            self.session.add(nuevo_envio)
            
            # Crear pago
            nuevo_pago = Pago(
                id_pedido=nuevo_pedido.id_pedido,
                metodo_pago_pago="pendiente",  # TODO: Obtener método de pago del cliente
                estado_pago_pago="pendiente",
                fecha_pago_pago=datetime.utcnow(),
            )
            self.session.add(nuevo_pago)
            
            self.session.commit()
            
            return self.obtener_pedido(nuevo_pedido.id_pedido)
        
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al crear pedido: {str(e)}")

    def obtener_pedido(self, pedido_id: int) -> PedidoResponse:
        """Obtener un pedido por ID"""
        try:
            from sqlmodel import select
            pedido = self.session.exec(
                select(Pedido).where(Pedido.id_pedido == pedido_id)
            ).first()
            
            if not pedido:
                raise ValueError(f"Pedido {pedido_id} no encontrado")
            
            return PedidoResponse.from_orm(pedido)
        except Exception as e:
            raise ValueError(f"Error al obtener pedido: {str(e)}")

    def obtener_pedidos_usuario(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        estado_filtro: str = None,
    ) -> list[PedidoResponse]:
        """Obtener pedidos del usuario con paginación y filtros"""
        try:
            from sqlmodel import select
            query = select(Pedido).where(
                Pedido.id_usuario == user_id
            ).order_by(Pedido.fecha_pedido_pedido.desc())
            
            if estado_filtro:
                query = query.where(Pedido.estado_pedido_pedido == estado_filtro)
            
            pedidos = self.session.exec(query.offset(skip).limit(limit)).all()
            
            return [PedidoResponse.from_orm(p) for p in pedidos]
        except Exception as e:
            # Retornar lista vacía si hay error en lugar de fallar
            return []

    def cancelar_pedido(self, pedido_id: int) -> dict:
        """Cancelar un pedido (solo si está pendiente)"""
        try:
            pedido = self.session.query(Pedido).filter(
                Pedido.id_pedido == pedido_id
            ).first()
            
            if not pedido:
                raise ValueError(f"Pedido {pedido_id} no encontrado")
            
            if pedido.estado_pedido != "pendiente":
                raise ValueError(
                    f"Solo se pueden cancelar pedidos pendientes. "
                    f"Estado actual: {pedido.estado_pedido}"
                )
            
            # Cambiar estado a cancelada
            pedido.estado_pedido = "cancelada"
            
            # Restaurar stock de los productos
            detalles = self.session.query(DetallePedido).filter(
                DetallePedido.id_pedido == pedido_id
            ).all()
            
            for detalle in detalles:
                producto = self.session.query(Producto).filter(
                    Producto.id_producto == detalle.id_producto
                ).first()
                
                if producto:
                    producto.stock_producto += detalle.cantidad_detalle_pedido
            
            # Actualizar estado del pago
            pago = self.session.query(Pago).filter(
                Pago.id_pedido == pedido_id
            ).first()
            
            if pago:
                pago.estado_pago = "cancelado"
            
            self.session.commit()
            
            return {
                "pedido_id": pedido_id,
                "estado": "cancelada",
                "mensaje": "Pedido cancelado y stock restaurado",
            }
        
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al cancelar pedido: {str(e)}")

    def obtener_rastreo_pedido(self, pedido_id: int) -> dict:
        """Obtener información de rastreo de un pedido"""
        try:
            pedido = self.session.query(Pedido).filter(
                Pedido.id_pedido == pedido_id
            ).first()
            
            if not pedido:
                raise ValueError(f"Pedido {pedido_id} no encontrado")
            
            envio = self.session.query(Envio).filter(
                Envio.id_pedido == pedido_id
            ).first()
            
            pago = self.session.query(Pago).filter(
                Pago.id_pedido == pedido_id
            ).first()
            
            return {
                "pedido_id": pedido_id,
                "estado_pedido": pedido.estado_pedido,
                "fecha_pedido": pedido.fecha_pedido,
                "envio": {
                    "estado": envio.estado_envio if envio else None,
                    "fecha_envio": envio.fecha_envio if envio else None,
                    "fecha_entrega_esperada": envio.fecha_entrega_esperada if envio else None,
                    "numero_seguimiento": envio.numero_seguimiento_envio if envio else None,
                } if envio else {},
                "pago": {
                    "estado": pago.estado_pago if pago else None,
                    "monto": float(pago.monto_pago) if pago else None,
                    "fecha": pago.fecha_pago if pago else None,
                } if pago else {},
            }
        except Exception as e:
            raise ValueError(f"Error al obtener rastreo: {str(e)}")

