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