"""
Rutas de cupones y descuentos
"""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from dependencies.exceptions import (
    CuponInvalido,
    CuponExpirado,
    CuponAgotado,
)
from schemas.cupon import CuponResponse, CuponValidateResponse
from services.cupon_service import CuponService
from db.connection import get_session

router = APIRouter(prefix="/api/cupones", tags=["cupones"])


@router.get("/validate", response_model=CuponValidateResponse)
def validate_coupon(
    codigo: str = Query(..., min_length=1),
    monto_total: float = Query(..., gt=0),
    session: Session = Depends(get_session),
):
    """
    Validar un cupón sin aplicarlo
    - codigo: Código del cupón
    - monto_total: Monto total de la orden (para calcular descuento)
    
    Retorna:
    - es_valido: Boolean
    - descuento_porcentaje: Porcentaje de descuento
    - monto_descuento: Cantidad de dinero descontada
    - monto_final: Monto total con descuento aplicado
    """
    try:
        cupon_service = CuponService(session)
        
        # Validar cupón (sin aplicar)
        cupon = cupon_service.validar_cupon(codigo)
        
        # Calcular descnentos
        descuento_monto = cupon_service.calcular_descuento(
            monto_total=monto_total,
            descuento_porcentaje=cupon.descuento_porcentaje_cupon,
        )
        
        monto_final = cupon_service.calcular_monto_con_descuento(
            monto_total=monto_total,
            cupon=cupon,
        )
        
        return CuponValidateResponse(
            es_valido=True,
            cupon_id=cupon.id_cupon,
            codigo_cupon=cupon.codigo_cupon,
            descuento_porcentaje=cupon.descuento_porcentaje_cupon,
            monto_descuento=descuento_monto,
            monto_final=monto_final,
        )
    except ValueError as e:
        error_msg = str(e).lower()
        if "expirado" in error_msg:
            raise CuponExpirado(detail=str(e))
        elif "agotado" in error_msg:
            raise CuponAgotado(detail=str(e))
        else:
            raise CuponInvalido(detail=str(e))


@router.post("/apply", response_model=CuponValidateResponse)
def apply_coupon(
    codigo: str = Query(..., min_length=1),
    monto_total: float = Query(..., gt=0),
    session: Session = Depends(get_session),
):
    """
    Aplicar un cupón e incrementar su contador de uso
    - codigo: Código del cupón
    - monto_total: Monto total de la orden
    
    Nota: Solo se debe llamar cuando se confirma la orden
    """
    try:
        cupon_service = CuponService(session)
        
        # Aplicar cupón (incrementa contador)
        cupon = cupon_service.aplicar_cupon(codigo)
        
        # Calcular descuentos
        descuento_monto = cupon_service.calcular_descuento(
            monto_total=monto_total,
            descuento_porcentaje=cupon.descuento_porcentaje_cupon,
        )
        
        monto_final = cupon_service.calcular_monto_con_descuento(
            monto_total=monto_total,
            cupon=cupon,
        )
        
        return CuponValidateResponse(
            es_valido=True,
            cupon_id=cupon.id_cupon,
            codigo_cupon=cupon.codigo_cupon,
            descuento_porcentaje=cupon.descuento_porcentaje_cupon,
            monto_descuento=descuento_monto,
            monto_final=monto_final,
        )
    except ValueError as e:
        error_msg = str(e).lower()
        if "expirado" in error_msg:
            raise CuponExpirado(detail=str(e))
        elif "agotado" in error_msg:
            raise CuponAgotado(detail=str(e))
        else:
            raise CuponInvalido(detail=str(e))


@router.get("/{cupon_id}", response_model=CuponResponse)
def get_coupon(
    cupon_id: int,
    session: Session = Depends(get_session),
):
    """
    Obtener información de un cupón (admin only)
    """
    try:
        cupon_service = CuponService(session)
        cupon = cupon_service.obtener_cupon(cupon_id)
        return cupon
    except ValueError as e:
        raise CuponInvalido(detail=str(e))

