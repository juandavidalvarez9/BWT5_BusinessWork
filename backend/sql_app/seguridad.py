"""Guardado seguro de contraseñas con PBKDF2 (biblioteca estándar)."""
import hashlib
import hmac
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERACIONES = 310_000


def _resumen(clave: str, sal: str, iteraciones: int) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", clave.encode("utf-8"), bytes.fromhex(sal), iteraciones
    ).hex()


def crear_hash(clave: str) -> str:
    sal = secrets.token_hex(16)
    return f"{ALGORITMO}${ITERACIONES}${sal}${_resumen(clave, sal, ITERACIONES)}"


def verificar(clave: str, guardado: str) -> bool:
    try:
        algoritmo, iteraciones, sal, resumen = guardado.split("$")
        calculado = _resumen(clave, sal, int(iteraciones))
    except (AttributeError, ValueError):
        return False
    return algoritmo == ALGORITMO and hmac.compare_digest(calculado, resumen)
