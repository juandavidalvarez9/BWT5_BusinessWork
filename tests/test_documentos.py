from datetime import date, timedelta

import pytest


@pytest.fixture
def usuario(client):
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
    return "ana"


def documento(dias_para_vencer, notificacion=10, nombre="Registro sanitario"):
    return {
        "name_document": nombre,
        "expiracion": (date.today() + timedelta(days=dias_para_vencer)).isoformat(),
        "notificacion": notificacion,
        "descripcion": "Documento de prueba",
    }


def test_crear_documento_para_un_usuario(client, usuario):
    respuesta = client.post(f"/users/{usuario}/documents/", json=documento(60))

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["id_documento"] == 1
    assert cuerpo["Users_username"] == "ana"
    assert cuerpo["name_document"] == "Registro sanitario"


def test_documento_para_usuario_inexistente_responde_404_y_no_guarda(client):
    respuesta = client.post("/users/nadie/documents/", json=documento(60))

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "User not found"}
    assert client.get("/documents/").json() == []


def test_listar_documentos(client, usuario):
    client.post(f"/users/{usuario}/documents/", json=documento(60, nombre="Licencia"))
    client.post(f"/users/{usuario}/documents/", json=documento(30, nombre="Póliza"))

    nombres = [d["name_document"] for d in client.get("/documents/").json()]

    assert nombres == ["Licencia", "Póliza"]


def test_el_usuario_incluye_sus_documentos(client, usuario):
    client.post(f"/users/{usuario}/documents/", json=documento(60))

    documentos = client.get(f"/users/{usuario}").json()["documentss"]

    assert [d["name_document"] for d in documentos] == ["Registro sanitario"]


@pytest.mark.parametrize(
    "dias, estado",
    [(-1, "vencido"), (0, "por_vencer"), (10, "por_vencer"), (11, "vigente")],
)
def test_estado_segun_los_dias_que_faltan(client, usuario, dias, estado):
    respuesta = client.post(
        f"/users/{usuario}/documents/", json=documento(dias, notificacion=10)
    )

    assert respuesta.json()["dias_restantes"] == dias
    assert respuesta.json()["estado"] == estado


def test_dias_de_aviso_negativos_se_rechazan(client, usuario):
    respuesta = client.post(
        f"/users/{usuario}/documents/", json=documento(60, notificacion=-5)
    )

    assert respuesta.status_code == 422
