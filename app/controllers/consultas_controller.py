from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import consultas_service
from ..views.consultas import DesactivarRequest, DesactivarResponse, PersonaDetalle

router = APIRouter(prefix="/personas", tags=["búsquedas y filtros"])


@router.get(
    "/buscar/{termino}",
    response_model=List[PersonaDetalle],
    summary="Buscador general de personas",
    description=(
        "Busca el término dentro de `first_name`, `last_name` **o** `email` "
        "(operador OR). Los caracteres `%` y `_` se tratan como texto literal. "
        "Si no hay coincidencias retorna una lista vacía `[]`."
    ),
)
def buscar_personas(termino: str, db: Session = Depends(get_db)):
    return consultas_service.buscar_personas(db, termino)


@router.get(
    "/cumpleanios/mes/{numero_mes}",
    response_model=List[PersonaDetalle],
    summary="Cumpleaños del mes",
    description=(
        "Retorna las personas cuyo mes de nacimiento coincide con `numero_mes` "
        "(1 a 12), sin importar el año. Ordenadas por día de cumpleaños."
    ),
    responses={
        400: {"description": "El mes no es un entero entre 1 y 12."},
    },
)
def cumpleanios_del_mes(numero_mes: str, db: Session = Depends(get_db)):
    try:
        mes = int(numero_mes)
    except ValueError:
        mes = None
    if mes is None or not 1 <= mes <= 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El mes debe ser un entero entre 1 y 12.",
        )
    return consultas_service.cumpleanios_del_mes(db, mes)


@router.patch(
    "/bulk/desactivar",
    response_model=DesactivarResponse,
    summary="Desactivación masiva de personas",
    description=(
        "Marca `is_active = false` en una sola operación para una lista de ids "
        "(entre 1 y 100, enteros positivos). Los ids que no existen no hacen "
        "fallar la operación: se reportan en `no_encontrados`."
    ),
    responses={
        400: {"description": "La lista de ids está vacía o tiene más de 100 elementos."},
        422: {"description": "Algún id no es un entero positivo."},
    },
)
def desactivar_masivo(datos: DesactivarRequest, db: Session = Depends(get_db)):
    if not datos.ids or len(datos.ids) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La lista de ids debe tener entre 1 y 100 elementos.",
        )
    return consultas_service.desactivar_personas(db, datos.ids)