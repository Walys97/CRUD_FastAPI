from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import consultas_service
from ..views.consultas import PersonaDetalle

router = APIRouter(prefix="/personas", tags=["búsquedas y filtros"])


@router.get("/buscar/{termino}", response_model=List[PersonaDetalle])
def buscar_personas(termino: str, db: Session = Depends(get_db)):
    """Busca el término en nombre, apellido o email. Si no hay resultados retorna []."""
    return consultas_service.buscar_personas(db, termino)


@router.get("/cumpleanios/mes/{numero_mes}", response_model=List[PersonaDetalle])
def cumpleanios_del_mes(numero_mes: str, db: Session = Depends(get_db)):
    """Personas que cumplen años en el mes indicado (1-12)."""
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