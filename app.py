from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="API de Tarefas",
    description="API para gerenciar tarefas",
    version="1.0.0",
    contact={
        "name": "Pedro Godoy",
        "email":"pedrohenriquegoodoy@gmail.com"}
)

Minhas_Tarefas = {}

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

@app.post("/tarefas/")
def criar_tarefa(tarefa: Tarefa):
    if tarefa.nome in Minhas_Tarefas:
        raise HTTPException(status_code=400, detail="Tarefa já cadastrada")
    Minhas_Tarefas[tarefa.nome] = tarefa.dict()
    return {"message": "Tarefa criada com sucesso", "tarefa": tarefa}

@app.get("/tarefas")
def listar_tarefas():
    if not Minhas_Tarefas:
        return {"message": "Nenhuma tarefa cadastrada"}
    return {"tarefas": list(Minhas_Tarefas.values())}
    
@app.put("/tarefas/{nome_tarefa}")
def atualizar_tarefa(nome_tarefa: str, tarefa: Tarefa):
    if nome_tarefa not in Minhas_Tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    Minhas_Tarefas[nome_tarefa] = tarefa.dict()
    return {"message": "Tarefa atualizada com sucesso", "tarefa": tarefa}

@app.delete("/tarefas/{nome_tarefa}")
def deletar_tarefa(nome_tarefa: str):
    if nome_tarefa not in Minhas_Tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa = Minhas_Tarefas.pop(nome_tarefa)
    return {"message": "Tarefa removida com sucesso", "tarefa": tarefa}

