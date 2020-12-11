
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATE
from sqlalchemy.orm import relationship

from .database import Base


class Departamento(Base):
    __tablename__ = "departamentos"

    id_departamento = Column(Integer, primary_key=True, index=True)
    name_dep = Column(String, index=True)
    
    users = relationship("User", back_populates="owner")

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    name = Column(String)
    last_name = Column(String)
    celular = Column(Integer)
    dep_id_dep = Column(Integer, ForeignKey("departamentos.id_departamento"))
    password = Column(String)

    owner = relationship("Departamento", back_populates="users")
    documentss = relationship("Documents", back_populates="owner2")

class Documents(Base):
    __tablename__ = "documentos"

    id_documento = Column(Integer, primary_key=True, index=True)
    name_document = Column(String)
    expiracion = Column(DATE)
    notificacion = Column(Integer)
    descripcion = Column(String)
    Users_username = Column(String, ForeignKey("users.username"))

    owner2 = relationship("User", back_populates="documentss")
    