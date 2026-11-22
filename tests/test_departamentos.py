def test_la_lista_de_departamentos_empieza_vacia(client):
    respuesta = client.get("/departamentos/")

    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_crear_departamento(client):
    respuesta = client.post("/departamentos/", json={"name_dep": "Jurídica"})

    assert respuesta.status_code == 200
    assert respuesta.json() == {"id_departamento": 1, "name_dep": "Jurídica", "users": []}


def test_departamento_repetido_responde_400(client):
    client.post("/departamentos/", json={"name_dep": "Jurídica"})

    respuesta = client.post("/departamentos/", json={"name_dep": "Jurídica"})

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "El departamento ya existe"}


def test_la_lista_devuelve_los_departamentos_creados(client):
    client.post("/departamentos/", json={"name_dep": "Jurídica"})
    client.post("/departamentos/", json={"name_dep": "Calidad"})

    nombres = [d["name_dep"] for d in client.get("/departamentos/").json()]

    assert nombres == ["Jurídica", "Calidad"]
