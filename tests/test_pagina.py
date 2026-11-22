import pytest


def test_la_raiz_sirve_la_pagina_de_ingreso(client):
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    assert "text/html" in respuesta.headers["content-type"]
    assert "Business Work" in respuesta.text


@pytest.mark.parametrize("ruta", ["/css/style.css", "/js/loginmain.js", "/img/img1.svg"])
def test_los_recursos_de_la_pagina_se_sirven(client, ruta):
    assert client.get(ruta).status_code == 200
