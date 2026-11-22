import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# La cadena de conexión se lee del entorno para no versionar credenciales.
# Ejemplo: export DATABASE_URL="postgresql://usuario:clave@localhost/btw5"
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://usuario:clave@localhost/btw5"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
