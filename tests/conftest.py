import os

# Las pruebas usan una base SQLite en memoria; debe definirse antes de importar la aplicación.
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient

from backend.sql_app import models
from backend.sql_app.database import engine
from backend.sql_app.main import app


@pytest.fixture
def client():
    models.Base.metadata.drop_all(bind=engine)
    with TestClient(app) as cliente:  # el arranque de la aplicación crea las tablas
        yield cliente
