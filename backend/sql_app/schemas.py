import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field, computed_field

class DocumentsBase(BaseModel):
    name_document: str
    expiracion: datetime.date
    # Días de anticipación con los que el documento pasa a "por vencer".
    notificacion: int = Field(ge=0)
    descripcion: str


class DocumentsCreate(DocumentsBase):
    pass


class Documents(DocumentsBase):
    id_documento: int
    Users_username: str

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def dias_restantes(self) -> int:
        return (self.expiracion - datetime.date.today()).days

    @computed_field
    @property
    def estado(self) -> str:
        if self.dias_restantes < 0:
            return "vencido"
        if self.dias_restantes <= self.notificacion:
            return "por_vencer"
        return "vigente"


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

    model_config = ConfigDict(from_attributes=True)


class DepartamentoBase(BaseModel):
    name_dep: str


class DepartamentoCreate(DepartamentoBase):
    pass


class Departamento(DepartamentoBase):
    id_departamento: int

    users: List[User]=[]
    model_config = ConfigDict(from_attributes=True)


class Credenciales(BaseModel):
    username: str
    password: str


class Ingreso(BaseModel):
    username: str
    name: str
