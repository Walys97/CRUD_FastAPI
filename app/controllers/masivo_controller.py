from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db  # <-- copia la línea de persona_controller.py
from ..services import masivo_service
from ..views.masivo import PoblarRequest, PoblarResponse

router = APIRouter(prefix="/personas", tags=["masivo"])


@router.post("/poblar", response_model=PoblarResponse, status_code=201)
def poblar(datos: PoblarRequest, db: Session = Depends(get_db)):
    if datos.cantidad <= 0 or datos.cantidad > 1000:
        raise HTTPException(
            status_code=400,
            detail="La cantidad debe ser un entero entre 1 y 1000.",
        )
    creados = masivo_service.poblar_personas(db, datos.cantidad)
    return {"message": f"{creados} usuarios creados exitosamente", "status": 201}