from typing import Sequence

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models.persona import Persona


def personas_por_dominio(db: Session) -> dict[str, int]:
    """Cuenta cuántas personas hay por proveedor de correo (lo que va después del @)."""
    sql = text(
        """
        SELECT SUBSTRING_INDEX(email, '@', -1) AS dominio,
               COUNT(*)                        AS cantidad
        FROM personas
        GROUP BY dominio
        ORDER BY cantidad DESC, dominio
        """
    )
    return {fila.dominio: fila.cantidad for fila in db.execute(sql)}

def estadisticas_edad(db: Session) -> dict:
    """Edad promedio (1 decimal), mínima y máxima (años cumplidos) a partir de birth_date."""
    sql = text(
        """
        SELECT ROUND(AVG(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())), 1) AS edad_promedio,
               MIN(TIMESTAMPDIFF(YEAR, birth_date, CURDATE()))           AS edad_minima,
               MAX(TIMESTAMPDIFF(YEAR, birth_date, CURDATE()))           AS edad_maxima
        FROM personas
        WHERE birth_date IS NOT NULL
        """
    )
    fila = db.execute(sql).mappings().one()
    # Si la tabla está vacía, MySQL devuelve NULL en las tres columnas
    return {
        "edad_promedio": float(fila["edad_promedio"]) if fila["edad_promedio"] is not None else None,
        "edad_minima": int(fila["edad_minima"]) if fila["edad_minima"] is not None else None,
        "edad_maxima": int(fila["edad_maxima"]) if fila["edad_maxima"] is not None else None,
    }


def reporte_activos(db: Session) -> Sequence[Persona]:
    """Personas con is_active = true."""
    return db.query(Persona).filter(Persona.is_active.is_(True)).order_by(Persona.id).all()