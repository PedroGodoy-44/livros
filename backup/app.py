from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Task(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False


tasks: List[Task] = []


@app.post("/tasks/", response_model=Task)
def add_task(task: Task):
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=List[Task])
def list_tasks():
    return tasks


@app.put("/tasks/{task_nome}", response_model=Task)
def complete_task(task_nome: str):
    for task in tasks:
        if task.nome == task_nome:
            task.concluida = True
            return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.delete("/tasks/{task_nome}", response_model=Task)
def delete_task(task_nome: str):
    for index, task in enumerate(tasks):
        if task.nome == task_nome:
            return tasks.pop(index)
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


