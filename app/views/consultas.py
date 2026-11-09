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
    

class PersonaActivo(BaseModel):
    """Proyección reducida para el reporte de activos."""
    id: int
    email: str
    phone: str | None
    is_active: bool

    model_config = {"from_attributes": True}