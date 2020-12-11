from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(dep_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_usuario_departamento(db, username=user.username, password=user.password, email=user.email, name=user.name, last_name=user.last_name, celular=user.celular, dep_id_dep=dep_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_usuario_departamento(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.get("/users/{user_username}", response_model=schemas.User)
def read_user(user_username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_username=user_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_username}/documents/", response_model=schemas.Documents)
def create_document_for_user(user_username: str, documento: schemas.DocumentsCreate, db: Session = Depends(get_db)):
    return crud.create_document_user(db=db, documento=documento, User_username=user_username)

@app.post("/departamentos/", response_model=schemas.Departamento)
def create_departamento(dept: schemas.DepartamentoCreate, db: Session = Depends(get_db)):
    db_dept = crud.get_departamentos(db, name_dep=dept.name_dep)
    if db_dept:
        raise HTTPException(status_code=400, detail="El departamento ya existe")
    return crud.create_departamentos(db=db, dept=dept)

@app.get("/documents/", response_model=List[schemas.Documents])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documentos(db, skip=skip, limit=limit)
    return documents

@app.get("/departamentos/", response_model=List[schemas.Departamento])
def read_departamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departamentos = crud.get_documentos(db, skip=skip, limit=limit)
    return departamentos