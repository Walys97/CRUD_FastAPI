from pydantic import BaseModel


class EdadEstadisticas(BaseModel):
    """Respuesta de GET /personas/estadisticas/edad."""
    edad_promedio: float | None
    edad_minima: int | None
    edad_maxima: int | None

    

class PersonaActiva(BaseModel):
    """Proyección reducida para el reporte de activos: solo 4 campos."""
    id: int
    email: str
    phone: str | None
    is_active: bool

    model_config = {"from_attributes": True}