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