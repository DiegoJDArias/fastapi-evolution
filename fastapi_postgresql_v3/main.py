from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()  # type: ignore

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(30), nullable=False)
    task_completed = Column(Boolean, default=False, nullable=False)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,            # type: ignore
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    task_name: str = Field(min_length=4, max_length=30)

class TaskReplace(BaseModel):
    task_name: str = Field(min_length=4, max_length=30)
    task_completed: bool

class TaskUpdate(BaseModel):
    task_name: Optional[str] = Field(None, min_length=4, max_length=30)
    task_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    task_name: str
    task_completed: bool
    model_config = {"from_attributes": True}

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Conexión exitosa"}

@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    tarea = TaskDB(task_name=task.task_name)
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea

@app.get("/tasks", status_code=status.HTTP_200_OK, response_model=list[TaskResponse])
def get_all_task(db: Session = Depends(get_db)):
    tarea = db.query(TaskDB).all()
    return tarea

@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    tarea = db.query(TaskDB).filter(TaskDB.id == task_id).one_or_none()

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El task no existe")
    return tarea

@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def update_task(task_id: int, task: TaskReplace, db: Session = Depends(get_db)):
    tarea = db.query(TaskDB).filter(TaskDB.id == task_id).one_or_none()

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El task no existe")
    tarea.task_name = task.task_name
    tarea.task_completed = task.task_completed

    db.commit()
    db.refresh(tarea)
    return tarea

@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def update_task_by_id(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    if task.task_name is None and task.task_completed is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar"
        )

    tarea = db.query(TaskDB).filter(TaskDB.id == task_id).one_or_none()

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El task no existe")

    datos_actualizar = task.model_dump(exclude_unset=True)

    for clave, valor in datos_actualizar.items():
        setattr(tarea, clave, valor)

    db.commit()
    db.refresh(tarea)
    return tarea

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    tarea = db.query(TaskDB).filter(TaskDB.id == task_id).one_or_none()

    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El task no existe")
    db.delete(tarea)
    db.commit()
