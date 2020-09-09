from fastapi import FastAPI
from pydantic import BaseModel

class Tarefa(BaseModel):
    '''
    Modelo para as tarefas a serem criadas
    '''
    idTarefa: int
    description: str
    isDone: bool = False

app = FastAPI()

# Database local de tarefas
db = []

@app.post("/tarefa")
async def create_tarefa(new_tarefa: Tarefa):
    '''
    Cria nova tarefa
    '''
    db.append(new_tarefa)
    return new_tarefa

@app.get("/tarefas")
async def get_tarefas():
    '''
    Retorna todas as tarefas
    '''
    return db

@app.delete("/tarefa/remover")
async def remove_tarefa(idT: int):
    '''
    Remove uma tarefa a partir de um id
    '''
    for i in range(len(db)):
        if db[i].idTarefa == idT:
            del db[i]
    print("Tarefa removida com sucesso!")
    return db

@app.patch("/tarefa/status")
async def atualiza_status(idT: int):
    '''
    Atualiza o estado isDone de uma tarefa de id igual ao parametro idT
    '''
    for task in db:
        if task.idTarefa == idT:
            task.isDone = not(task.isDone)
    print("Task Done!")
    return db

@app.patch("/tarefa/descricao")
async def atualiza_desc(idT: int, descricao: str):
    '''
    Atualiza descrição de uma tarefa de id igual ao parametro idT
    '''
    for task in db:
        if task.idTarefa == idT:
            task.description = descricao
    print("Description Done!")
    return db

@app.get("/tarefas/notdone")
async def isnotdone():
    '''
    Entrega tarefas não finalizadas!
    '''
    doneTasks = []
    for task in db:
        if task.isDone == False:
            doneTasks.append(task)
    return doneTasks

@app.get("/tarefas/done")
async def done():
    '''
    Entrega tarefas finalizadas!
    '''
    undoneTasks = []
    for task in db:
        if task.isDone:
            undoneTasks.append(task)
    return undoneTasks