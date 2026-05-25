from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
tasks: list[dict] = []

count_id = 1

class TaskCreate(BaseModel):
    task: str = Field(min_length=4, max_length=30)

class TaskReplace(BaseModel):
    task: str = Field(min_length=4, max_length=30)
    completed: bool

class TaskUpdate(BaseModel):
    task: Optional[str] = Field(None, min_length=4, max_length=30)
    completed: Optional[bool] = None

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"Message": "servidor funcionando correctamente."}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global count_id
    diccionario = {"id": count_id, **task.model_dump(), "completed": False}
    count_id += 1
    tasks.append(diccionario)
    return diccionario

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task_by_id(id: int):
    for valor in tasks:
        if valor["id"] == id:
            return valor
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

@app.put("/tasks/{id}")
def update_task(id: int, task: TaskReplace):
    for valor in tasks:
        if valor["id"] == id:
            valor.update(task.model_dump())
            return valor
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

@app.patch("/tasks/{id}")
def update_task_by_id(id: int, task: TaskUpdate):
    if task.task is None and task.completed is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debes enviar al menos un campo para actualizar (task o completed)")

    for valor in tasks:
        if valor["id"] == id:
            valor.update(task.model_dump(exclude_unset=True))
            return valor
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(id: int):

    for index, valor in enumerate(tasks):
        if valor["id"] == id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
