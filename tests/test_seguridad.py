from backend.sql_app import seguridad


def test_el_hash_no_contiene_la_clave():
    assert "secreta123" not in seguridad.crear_hash("secreta123")


def test_dos_hashes_de_la_misma_clave_son_distintos():
    assert seguridad.crear_hash("secreta123") != seguridad.crear_hash("secreta123")


def test_verificar_acepta_la_clave_correcta():
    assert seguridad.verificar("secreta123", seguridad.crear_hash("secreta123"))


def test_verificar_rechaza_otra_clave():
    assert not seguridad.verificar("otra", seguridad.crear_hash("secreta123"))


def test_verificar_rechaza_un_valor_guardado_mal_formado():
    assert not seguridad.verificar("secreta123", "texto-sin-formato")
