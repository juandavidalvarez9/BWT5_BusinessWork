from backend.sql_app import datos_demo
from backend.sql_app.database import SessionLocal


def cargar():
    with SessionLocal() as db:
        return datos_demo.cargar(db)


def test_los_datos_de_demostracion_permiten_ingresar(client):
    assert cargar() is True

    respuesta = client.post("/login", json={"username": "demo", "password": "demo1234"})

    assert respuesta.status_code == 200


def test_la_demostracion_trae_un_documento_en_cada_estado(client):
    cargar()

    documentos = client.get("/users/demo").json()["documentss"]

    assert sorted(d["estado"] for d in documentos) == ["por_vencer", "vencido", "vigente"]


def test_cargar_dos_veces_no_duplica(client):
    cargar()

    assert cargar() is False
    assert len(client.get("/users/").json()) == 1
    assert len(client.get("/documents/").json()) == 3
