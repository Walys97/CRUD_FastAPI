from pydantic import BaseModel


class EdadEstadisticas(BaseModel):
    """Respuesta de GET /personas/estadisticas/edad."""
    edad_promedio: float | None
    edad_minima: int | None
    edad_maxima: int | None