from typing import Sequence

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..models.persona import Persona


def _escapar_like(texto: str) -> str:
    """Escapa los comodines de LIKE para buscar el texto de forma literal."""
    return (
        texto.replace("!", "!!")
        .replace("%", "!%")
        .replace("_", "!_")
    )


def buscar_personas(db: Session, termino: str) -> Sequence[Persona]:
    """Busca el término en first_name, last_name O email (LIKE %termino%)."""
    patron = f"%{_escapar_like(termino)}%"
    return (
        db.query(Persona)
        .filter(
            or_(
                Persona.first_name.like(patron, escape="!"),
                Persona.last_name.like(patron, escape="!"),
                Persona.email.like(patron, escape="!"),
            )
        )
        .order_by(Persona.id)
        .all()
    )


def cumpleanios_del_mes(db: Session, mes: int) -> Sequence[Persona]:
    """Personas cuyo mes de nacimiento es `mes`, sin importar el año."""
    return (
        db.query(Persona)
        .filter(func.month(Persona.birth_date) == mes)
        .order_by(func.day(Persona.birth_date), Persona.id)
        .all()
    )


def desactivar_personas(db: Session, ids: list[int]) -> dict:
    """Desactiva en una sola operación los ids que existen y reporta los que no."""
    ids_unicos = list(dict.fromkeys(ids))  # quita repetidos conservando el orden
    filas = db.query(Persona.id).filter(Persona.id.in_(ids_unicos)).all()
    existentes = {fila.id for fila in filas}

    desactivados = [i for i in ids_unicos if i in existentes]
    no_encontrados = [i for i in ids_unicos if i not in existentes]

    if desactivados:
        db.query(Persona).filter(Persona.id.in_(desactivados)).update(
            {Persona.is_active: False}, synchronize_session=False
        )
        db.commit()

    return {
        "message": "Operación completada.",
        "desactivados": desactivados,
        "no_encontrados": no_encontrados,
        "total_desactivados": len(desactivados),
    }