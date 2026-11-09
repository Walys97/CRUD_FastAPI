from datetime import date

from pydantic import BaseModel


class PersonaDetalle(BaseModel):
    """Persona sin created_at, para búsquedas y cumpleaños."""
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str | None
    birth_date: date | None
    is_active: bool
    notes: str | None

    model_config = {"from_attributes": True}


class DesactivarRequest(BaseModel):
    """Body del PATCH: lista de ids a desactivar."""
    ids: list[int]


class DesactivarResponse(BaseModel):
    """Respuesta del PATCH: qué se desactivó y qué no se encontró."""
    message: str
    desactivados: list[int]
    no_encontrados: list[int]
    total_desactivados: int