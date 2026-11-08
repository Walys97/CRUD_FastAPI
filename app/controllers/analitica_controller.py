from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import analitica_service

router = APIRouter(prefix="/personas", tags=["analítica"])


@router.get("/estadisticas/dominios", response_model=Dict[str, int])
def estadisticas_dominios(db: Session = Depends(get_db)):
    """Cantidad de personas por proveedor de correo."""
    return analitica_service.personas_por_dominio(db)