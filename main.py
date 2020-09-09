from fastapi import FastAPI
from pydantic import BaseModel

class Tarefa(BaseModel):
    idTarefa: int
    description: str
    isDone: bool

app = FastAPI()

db = []

@app.post("/tarefa/")
async def create_tarefa(new_tarefa: Tarefa):
    db.append(new_tarefa)
    return new_tarefa

@app.get("/tarefas/")
async def get_tarefas():
    return db