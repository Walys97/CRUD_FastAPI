import random
import unicodedata

from faker import Faker
from sqlalchemy.orm import Session

from ..models.persona import Persona

fake = Faker("es_CO")
DOMINIOS = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com"]


def _limpiar(texto: str) -> str:
    """Quita tildes, espacios y mayúsculas para armar el email."""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return texto.lower().replace(" ", "")


def _telefono() -> str:
    """Celular colombiano con el formato +57 3XX XXX XXXX."""
    return f"+57 3{random.randint(0, 2)}{random.randint(0, 9)} {random.randint(100, 999)} {random.randint(1000, 9999)}"