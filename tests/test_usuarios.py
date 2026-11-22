import pytest
from sqlalchemy import BigInteger

from backend.sql_app import models, seguridad
from backend.sql_app.database import SessionLocal

ANA = {
    "username": "ana",
    "email": "ana@example.com",
    "name": "Ana",
    "last_name": "Pérez",
    "celular": 3001234567,
    "password": "secreta123",
}


@pytest.fixture
def departamento(client):
    respuesta = client.post("/departamentos/", json={"name_dep": "Jurídica"})
    return respuesta.json()["id_departamento"]


def crear(client, dep_id, **cambios):
    return client.post("/users/", params={"dep_id": dep_id}, json={**ANA, **cambios})


def test_crear_usuario_no_devuelve_la_clave(client, departamento):
    respuesta = crear(client, departamento)

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "username": "ana",
        "email": "ana@example.com",
        "name": "Ana",
        "last_name": "Pérez",
        "celular": 3001234567,
        "documentss": [],
    }


def test_la_clave_se_guarda_con_hash(client, departamento):
    crear(client, departamento)

    with SessionLocal() as db:
        guardada = db.get(models.User, "ana").password

    assert guardada != "secreta123"
    assert seguridad.verificar("secreta123", guardada)


def test_usuario_repetido_responde_400(client, departamento):
    crear(client, departamento)

    respuesta = crear(client, departamento, email="otro@example.com")

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "El usuario ya existe"}


def test_correo_repetido_responde_400(client, departamento):
    crear(client, departamento)

    respuesta = crear(client, departamento, username="ana2")

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "El correo ya está registrado"}


def test_departamento_inexistente_responde_404_y_no_guarda(client):
    respuesta = crear(client, 99)

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "El departamento no existe"}
    assert client.get("/users/").json() == []


def test_listar_usuarios(client, departamento):
    crear(client, departamento)
    crear(client, departamento, username="luis", email="luis@example.com")

    nombres = [u["username"] for u in client.get("/users/").json()]

    assert nombres == ["ana", "luis"]


def test_consultar_usuario(client, departamento):
    crear(client, departamento)

    respuesta = client.get("/users/ana")

    assert respuesta.status_code == 200
    assert respuesta.json()["email"] == "ana@example.com"


def test_usuario_inexistente_responde_404(client):
    respuesta = client.get("/users/nadie")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "User not found"}


def test_el_celular_admite_numeros_de_diez_digitos():
    # En PostgreSQL un entero de 32 bits se desborda con 3001234567; SQLite no lo reproduce.
    assert isinstance(models.User.__table__.c.celular.type, BigInteger)
