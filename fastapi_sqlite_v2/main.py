from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3


connection = sqlite3.connect("database.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS tasks
               (
                   id        INTEGER PRIMARY KEY AUTOINCREMENT,
                   task      TEXT    NOT NULL,
                   completed BOOLEAN NOT NULL DEFAULT 0
               )
               """)
app = FastAPI()


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
    cursor.execute(""" INSERT INTO tasks (task)
                       VALUES (?)""", (task.task,))
    connection.commit()
    id_generado = cursor.lastrowid
    return {"id": id_generado, "task": task.task, "completed": False}

@app.get("/tasks")
def get_all_tasks():
    cursor.execute("SELECT * FROM tasks")
    filas = cursor.fetchall()
    lista_tareas = []

    for fila in filas:
        lista_tareas.append({
            "id": fila[0],
            "task": fila[1],
            "completed": bool(fila[2])
        })
    return lista_tareas

@app.get("/tasks/{id}")
def get_task_by_id(id: int):
    cursor.execute(""" SELECT *
                       FROM tasks
                       WHERE id = ?""", (id,))
    fila = cursor.fetchone()

    if fila is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return {"id": fila[0], "task": fila[1], "completed": bool(fila[2])}


@app.put("/tasks/{id}")
def update_task(id: int, task: TaskReplace):
    cursor.execute(''' UPDATE tasks
                       SET task      = ?,
                           completed = ?
                       WHERE id = ?''', (task.task, task.completed, id,))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    connection.commit()
    return {"id": id, "task": task.task, "completed": task.completed}


@app.patch("/tasks/{id}")
def update_task_by_id(id: int, task: TaskUpdate):
    if task.task is None and task.completed is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Debes enviar al menos un campo para actualizar (task o completed)")

    if task.task is not None and task.completed is not None:
        cursor.execute(""" UPDATE tasks
                           SET task      = ?,
                               completed = ?
                           WHERE id = ?""", (task.task, task.completed, id,))
    elif task.task is not None:
        cursor.execute(""" UPDATE tasks
                           SET task = ?
                           WHERE id = ?""", (task.task, id,))
    else:
        cursor.execute(""" UPDATE tasks
                           SET completed = ?
                           WHERE id = ?""", (task.completed, id,))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    connection.commit()

    cursor.execute(""" SELECT *
                       FROM tasks
                       WHERE id = ?""", (id,))
    fila = cursor.fetchone()

    return {"id": fila[0], "task": fila[1], "completed": bool(fila[2])}


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(id: int):
    cursor.execute(""" DELETE
                       FROM tasks
                       WHERE id = ?""", (id,))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    connection.commit()
    return None
