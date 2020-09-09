from fastapi import FastAPI
from pydantic import BaseModel

class Tarefa(BaseModel):
    idTarefa: int
    description: str
    isDone: bool

app = FastAPI()

db = []

@app.post("/tarefa")
async def create_tarefa(new_tarefa: Tarefa):
    db.append(new_tarefa)
    return new_tarefa

@app.get("/tarefas")
async def get_tarefas():
    '''
    Retorna todas as tarefas
    '''
    return db

@app.get("/tarefas/notdone")
async def isnotdone():
    doneTasks = []
    for task in db:
        if task.isDone == False:
            doneTasks.append(task)
    return doneTasks

@app.get("/tarefas/done")
async def done():
    undoneTasks = []
    for task in db:
        if task.isDone:
            undoneTasks.append(task)
    return undoneTasks