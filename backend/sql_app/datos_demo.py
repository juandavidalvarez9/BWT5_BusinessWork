"""Datos de demostración.

Uso: python -m backend.sql_app.datos_demo
"""
from datetime import date, timedelta

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

USUARIO = "demo"
CLAVE = "demo1234"
DEPARTAMENTO = "Jurídica"

# (nombre, días hasta el vencimiento, días de aviso, descripción)
DOCUMENTOS = [
    ("Póliza de responsabilidad civil", -12, 30, "Ya venció: hay que renovarla."),
    ("Registro sanitario", 9, 30, "Entra en la ventana de aviso de 30 días."),
    ("Certificado de existencia", 180, 30, "Vigente por varios meses."),
]


def cargar(db: Session) -> bool:
    """Crea los datos de demostración si no existen. Devuelve True si creó algo."""
    if crud.get_user(db, user_username=USUARIO):
        return False

    departamento = crud.get_departamento_por_nombre(db, name_dep=DEPARTAMENTO)
    if departamento is None:
        departamento = crud.create_departamento(
            db, schemas.DepartamentoCreate(name_dep=DEPARTAMENTO)
        )

    crud.create_user(
        db,
        schemas.UserCreate(
            username=USUARIO,
            email="demo@example.com",
            name="Usuario",
            last_name="Demo",
            celular=3001234567,
            password=CLAVE,
        ),
        dep_id=departamento.id_departamento,
    )

    hoy = date.today()
    for nombre, dias, aviso, descripcion in DOCUMENTOS:
        crud.create_document_user(
            db,
            schemas.DocumentsCreate(
                name_document=nombre,
                expiracion=hoy + timedelta(days=dias),
                notificacion=aviso,
                descripcion=descripcion,
            ),
            user_username=USUARIO,
        )
    return True


def main():
    models.Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if cargar(db):
            print(f"Datos de demostración creados. Usuario: {USUARIO} / Clave: {CLAVE}")
        else:
            print("Los datos de demostración ya existían.")


if __name__ == "__main__":
    main()
