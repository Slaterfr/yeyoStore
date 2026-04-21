"""
BaseRepository - Patrón genérico CRUD
Clase base para todos los repositories
Proporciona métodos comunes: get_by_id, get_all, create, update, delete
"""
from typing import TypeVar, Generic, Type, Optional, List
from sqlmodel import Session, select
from dependencies.exceptions import ErrorValidacion

# TypeVar genérico para cualquier modelo SQLModel
T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Repository genérico con CRUD básico
    
    Uso:
        class UsuarioRepository(BaseRepository[Usuario]):
            def __init__(self, session: Session):
                super().__init__(session, Usuario)
    """

    def __init__(self, session: Session, model: Type[T]):
        """
        Inicializa el repository
        
        Args:
            session: Sesión de SQLModel
            model: Clase del modelo (ej: Usuario, Producto)
        """
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        """Obtiene un registro por ID"""
        try:
            statement = select(self.model).where(self.model.id == id)
            return self.session.exec(statement).first()
        except Exception as e:
            raise ErrorValidacion(f"Error al obtener registro: {str(e)}")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene todos los registros con paginación"""
        try:
            statement = select(self.model).offset(skip).limit(limit)
            return self.session.exec(statement).all()
        except Exception as e:
            raise ErrorValidacion(f"Error al obtener registros: {str(e)}")

    def create(self, obj_in: T) -> T:
        """Crea un nuevo registro"""
        try:
            self.session.add(obj_in)
            self.session.commit()
            self.session.refresh(obj_in)
            return obj_in
        except Exception as e:
            self.session.rollback()
            raise ErrorValidacion(f"Error al crear registro: {str(e)}")

    def update(self, obj_in: T) -> T:
        """Actualiza un registro existente"""
        try:
            self.session.merge(obj_in)
            self.session.commit()
            return obj_in
        except Exception as e:
            self.session.rollback()
            raise ErrorValidacion(f"Error al actualizar registro: {str(e)}")

    def delete(self, id: int) -> bool:
        """Elimina un registro por ID"""
        try:
            obj = self.get_by_id(id)
            if not obj:
                return False
            self.session.delete(obj)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ErrorValidacion(f"Error al eliminar registro: {str(e)}")

    def count(self) -> int:
        """Cuenta el total de registros"""
        try:
            statement = select(self.model)
            return len(self.session.exec(statement).all())
        except Exception as e:
            raise ErrorValidacion(f"Error al contar registros: {str(e)}")
