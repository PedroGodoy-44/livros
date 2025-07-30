from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

Meus_Livros = {}

class Livro(BaseModel):
    nome: str
    autor: str
    ano_livro: int

@app.post("/Adiciona/")  # Remova response_model=Livro
def post_livro(livro: Livro):
    if livro.nome in Meus_Livros:
        raise HTTPException(status_code=400, detail="Livro já cadastrado")
    else:  
        Meus_Livros[livro.nome] = livro.dict()
        return {"message": "Livro adicionado com sucesso", "livro": livro.dict()}

@app.get("/livros")
def get_livro():
    if not Meus_Livros:
        return {"message": "Nenhum livro cadastrado"}
    else:
        return {"livros": list(Meus_Livros.values())}
    
@app.put("/atualiza/{nome_livro}")
def put_livro(nome_livro: str, livro: Livro):
    if nome_livro not in Meus_Livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    else:
        Meus_Livros[nome_livro] = livro.dict()
        return {"message": "Livro atualizado com sucesso", "livro": livro.dict()}

@app.delete("/livros/{nome_livro}")
def delete_livro(nome_livro: str):
    if nome_livro not in Meus_Livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    livro = Meus_Livros.pop(nome_livro)
    return {"message": "Livro removido com sucesso", "livro": livro}

