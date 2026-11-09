import random
import unicodedata
import csv
import io

from faker import Faker
from sqlalchemy.orm import Session

from ..models.persona import Persona

fake = Faker("es_CO")
DOMINIOS = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com"]
NOTAS = ["Cliente frecuente",
    "Prefiere contacto por correo",
    "Pendiente de verificación",
    "Solicitó información adicional",
    "Contactar en horario de la tarde",]

def _limpiar(texto: str) -> str:
    """Quita tildes, espacios y mayúsculas para armar el email."""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return texto.lower().replace(" ", "")


def _telefono() -> str:
    """Celular colombiano con el formato +57 3XX XXX XXXX."""
    return f"+57 3{random.randint(0, 2)}{random.randint(0, 9)} {random.randint(100, 999)} {random.randint(1000, 9999)}"

def poblar_personas(db: Session, cantidad: int) -> int:
    # Emails que ya existen, para no repetirlos (la columna es UNIQUE)
    emails_usados = {fila[0] for fila in db.query(Persona.email).all()}
    nuevas = []

    for _ in range(cantidad):
        nombre = fake.first_name()
        apellido = fake.last_name()
        base = f"{_limpiar(nombre)}.{_limpiar(apellido)}"
        dominio = random.choice(DOMINIOS)

        email = f"{base}@{dominio}"
        while email in emails_usados:
            email = f"{base}{random.randint(1, 9999)}@{dominio}"
        emails_usados.add(email)

        nuevas.append(
            Persona(
                first_name=nombre,
                last_name=apellido,
                email=email,
                phone=_telefono(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=85),
                is_active=random.choice([True, False]),
                notes=random.choice([None, random.choice(NOTAS)]),
            )
        )

    db.add_all(nuevas)
    db.commit()
    return len(nuevas)

COLUMNAS_CSV = [
    "id", "first_name", "last_name", "email",
    "phone", "birth_date", "is_active", "notes",
]


def generar_csv(db: Session) -> str:
    personas = db.query(Persona).order_by(Persona.id).all()
    salida = io.StringIO()
    salida.write("\ufeff")  #Pa que no salgan raras las tildes en Excel
    escritor = csv.writer(salida)
    escritor.writerow(COLUMNAS_CSV)
    for p in personas:
        escritor.writerow([
            p.id, p.first_name, p.last_name, p.email, p.phone,
            p.birth_date, p.is_active, p.notes or "",
        ])
    return salida.getvalue()