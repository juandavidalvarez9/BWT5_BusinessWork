import datetime
from typing import List, Optional

from pydantic import BaseModel

class DocumentsBase(BaseModel):
    name_document: str
    expiracion: datetime.date
    notificacion: int
    descripcion: str


class DocumentsCreate(DocumentsBase):
    pass


class Documents(DocumentsBase):
    id_documento: int
    Users_username: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    name: str
    last_name: str
    celular: int


class UserCreate(UserBase):
    password: str



class User(UserBase):
    username: str
    email: str
    name: str
    last_name: str
    celular: int
    documentss: List[Documents]=[]

    class Config:
        orm_mode = True


class DepartamentoBase(BaseModel):
    name_dep: str


class DepartamentoCreate(DepartamentoBase):
    pass


class Departamento(DepartamentoBase):
    id_departamento: int

    users: List[User]=[]
    class Config:
        orm_mode = True






