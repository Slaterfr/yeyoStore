"""
ProductoService
Servicio de gestión de productos y catálogo
"""
from sqlmodel import Session, select
from models.producto import Producto
from models.foto_producto import FotoProducto
from models.producto_talla import ProductoTalla
from schemas.producto import ProductoCreate, ProductoUpdate
from dependencies.exceptions import ProductoNoEncontrado, ErrorValidacion
from typing import List, Optional
from decimal import Decimal


class ProductoService:
    """Servicio de gestión de productos"""

    def __init__(self, session: Session):
        self.session = session

    def crear_producto(self, producto_create: ProductoCreate) -> Producto:
        """Crea un nuevo producto (admin)"""
        nuevo_producto = Producto(
            nombre_producto=producto_create.nombre_producto,
            descripcion_producto=producto_create.descripcion_producto,
            precio_producto=producto_create.precio_producto,
            categoria_producto=producto_create.categoria_producto,
            stock_producto=producto_create.stock_producto,
            marca_producto=producto_create.marca_producto,
            promedio_calificacion_producto=0.0,
        )

        self.session.add(nuevo_producto)
        self.session.commit()
        self.session.refresh(nuevo_producto)

        return nuevo_producto

    def obtener_producto(self, producto_id: int) -> Producto:
        """Obtiene un producto por ID"""
        producto = self.session.get(Producto, producto_id)

        if not producto:
            raise ProductoNoEncontrado()

        return producto

    def obtener_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """Obtiene productos de una categoría"""
        statement = select(Producto).where(
            Producto.categoria_producto == categoria
        )
        return self.session.exec(statement).all()

    def obtener_todos_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """Obtiene todos los productos con paginación"""
        statement = select(Producto).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def buscar_productos_avanzado(
        self,
        q: Optional[str] = None,
        categoria: Optional[str] = None,
        precio_min: Optional[float] = None,
        precio_max: Optional[float] = None,
        talla: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Producto]:
        """
        Búsqueda avanzada de productos con filtros
        - q: término de búsqueda en nombre o descripción
        - categoria: filtrar por categoría
        - precio_min: precio mínimo
        - precio_max: precio máximo
        - talla: filtrar por talla disponible (valor_talla)
        """
        statement = select(Producto)

        # Filtro por búsqueda de texto
        if q:
            from sqlalchemy import or_
            statement = statement.where(
                or_(
                    Producto.nombre_producto.ilike(f"%{q}%"),
                    Producto.descripcion_producto.ilike(f"%{q}%"),
                )
            )

        # Filtro por categoría
        if categoria:
            statement = statement.where(Producto.categoria_producto == categoria)

        # Filtro por rango de precio
        if precio_min is not None:
            statement = statement.where(Producto.precio_producto >= precio_min)
        if precio_max is not None:
            statement = statement.where(Producto.precio_producto <= precio_max)

        # Filtro por talla (requiere JOIN con ProductoTalla → Talla)
        if talla:
            from models.talla import Talla
            statement = statement.join(ProductoTalla).join(Talla).where(
                Talla.valor_talla == talla
            ).distinct()

        # Aplicar paginación
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def actualizar_producto(self, producto_id: int, producto_update: ProductoUpdate) -> Producto:
        """Actualiza un producto (admin)"""
        producto = self.obtener_producto(producto_id)

        if producto_update.nombre_producto:
            producto.nombre_producto = producto_update.nombre_producto

        if producto_update.descripcion_producto:
            producto.descripcion_producto = producto_update.descripcion_producto

        if producto_update.precio_producto:
            producto.precio_producto = producto_update.precio_producto

        if producto_update.categoria_producto:
            producto.categoria_producto = producto_update.categoria_producto

        if producto_update.stock_producto is not None:
            producto.stock_producto = producto_update.stock_producto

        if producto_update.marca_producto:
            producto.marca_producto = producto_update.marca_producto

        self.session.add(producto)
        self.session.commit()
        self.session.refresh(producto)

        return producto

    def actualizar_rating_promedio(self, producto_id: int) -> None:
        """Recalcula el rating promedio del producto"""
        producto = self.obtener_producto(producto_id)
        
        from models.reseña import Reseña
        statement = select(Reseña).where(Reseña.id_producto == producto_id)
        reseñas = self.session.exec(statement).all()

        if reseñas:
            promedio = sum(r.calificacion_reseña for r in reseñas) / len(reseñas)
            producto.promedio_calificacion_producto = round(float(promedio), 2)
        else:
            producto.promedio_calificacion_producto = 0.0

        self.session.add(producto)
        self.session.commit()

    def obtener_fotos_producto(self, producto_id: int) -> List[FotoProducto]:
        """Obtiene todas las fotos de un producto"""
        statement = select(FotoProducto).where(
            FotoProducto.id_producto == producto_id
        ).order_by(FotoProducto.orden_foto_producto)

        return self.session.exec(statement).all()

