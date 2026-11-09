from typing import Sequence

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..models.persona import Persona


def buscar_personas(db: Session, termino: str) -> Sequence[Persona]:
    """Busca el término en first_name, last_name O email (LIKE %termino%)."""
    patron = f"%{termino}%"
    return (
        db.query(Persona)
        .filter(
            or_(
                Persona.first_name.like(patron),
                Persona.last_name.like(patron),
                Persona.email.like(patron),
            )
        )
        .order_by(Persona.id)
        .all()
    )