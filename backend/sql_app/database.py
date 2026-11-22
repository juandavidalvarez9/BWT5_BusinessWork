import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# Por defecto se usa un archivo SQLite local: la aplicación corre sin instalar nada.
# Para PostgreSQL: export DATABASE_URL="postgresql://usuario:clave@localhost/btw5"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./btw5.db")

opciones = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    opciones["connect_args"] = {"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL in ("sqlite://", "sqlite:///:memory:"):
        # Base en memoria: una sola conexión compartida para que los datos se conserven.
        opciones["poolclass"] = StaticPool

engine = create_engine(SQLALCHEMY_DATABASE_URL, **opciones)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
