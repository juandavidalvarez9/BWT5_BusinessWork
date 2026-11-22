import pytest

CLAVE_MALA = {"detail": "Usuario o contraseña incorrectos."}


@pytest.fixture
def ana(client):
    departamento = client.post("/departamentos/", json={"name_dep": "Jurídica"}).json()
    client.post(
        "/users/",
        params={"dep_id": departamento["id_departamento"]},
        json={
            "username": "ana",
            "email": "ana@example.com",
            "name": "Ana",
            "last_name": "Pérez",
            "celular": 3001234567,
            "password": "secreta123",
        },
    )


def test_ingreso_correcto(client, ana):
    respuesta = client.post("/login", json={"username": "ana", "password": "secreta123"})

    assert respuesta.status_code == 200
    assert respuesta.json() == {"username": "ana", "name": "Ana"}


def test_clave_incorrecta_responde_401(client, ana):
    respuesta = client.post("/login", json={"username": "ana", "password": "otra"})

    assert respuesta.status_code == 401
    assert respuesta.json() == CLAVE_MALA


def test_usuario_inexistente_responde_igual_que_clave_incorrecta(client, ana):
    respuesta = client.post("/login", json={"username": "nadie", "password": "secreta123"})

    assert respuesta.status_code == 401
    assert respuesta.json() == CLAVE_MALA


def test_ingreso_sin_clave_se_rechaza(client, ana):
    respuesta = client.post("/login", json={"username": "ana"})

    assert respuesta.status_code == 422
