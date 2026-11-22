from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_username: str):
    return db.query(models.User).filter(models.User.username== user_username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, user_username: str):
    return db.query(models.User).offset(user_username).all()

    
def get_departamento_por_nombre(db: Session, name_dep: str):
    return db.query(models.Departamento).filter(models.Departamento.name_dep == name_dep).first()


def get_departamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Departamento).offset(skip).limit(limit).all()


def create_departamento(db: Session, departamento: schemas.DepartamentoCreate):
    db_departamento = models.Departamento(name_dep=departamento.name_dep)
    db.add(db_departamento)
    db.commit()
    db.refresh(db_departamento)
    return db_departamento


def create_usuario_departamento(db: Session, user: schemas.UserCreate):
    s_password= user.password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_documentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Documents).offset(skip).limit(limit).all()


def create_document_user(db: Session, documento: schemas.DocumentsCreate, user_username: str):
    db_documents = models.Documents(**documento.dict(), Users_username=user_username)
    db.add(db_documents)
    db.commit()
    db.refresh(db_documents)
    return db_documents