'''
ADICIONAR RESPONSE MODEL PARA TODAS AS REQS
'''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uuid
from fastapi.encoders import jsonable_encoder

# ===== MODELS ===== #

class Tarefa(BaseModel):
    '''
    Modelo para as tarefas a serem criadas
    '''
    description: str = Field(default="Sem descrição", example="Finalizar APS1 de Megadados", title="A tarefa a ser realizada")
    isDone: bool = Field( default=False , title="Status da tarefa")

# ===== DOC METADATA ===== #

tags_metadata = [
    {
        "name": "Tarefas",
        "description": "Requests relativas à criação, edição e remoção de tarefas da lista.",
    }
]


# ===== API DECLARATION ===== #

app = FastAPI(
    title="APS1 Megadados",
    description="Esta entrega consiste em uma API simples para manusear uma lista de tarefas",
    version="1.0.0",
    openapi_tags=tags_metadata    
)

# Database local de tarefas
db = {}

@app.post("/tarefas", tags=["Tarefas"], description="Cria uma nova tarefa", name="Criar tarefa")
async def create_tarefa(new_tarefa: Tarefa):
    '''
    Cria nova tarefa
    '''
    taskId = str(uuid.uuid1())
    db[taskId]=new_tarefa.dict()
    return taskId

@app.get("/tarefas", tags=["Tarefas"], name="Listar tarefas", description="Permite listar todas as tarefas, somente as feitas ou somente as não feitas.")
async def get_tarefas(completed: bool = None ):
    '''
    Retorna todas as tarefas
    '''
    tasks = {}
    if completed == True:
        for taskId in db:
            if db[taskId]["isDone"]:
                tasks[taskId]=db[taskId]
        return tasks
    elif completed == False:
        for taskId in db:
            if db[taskId]["isDone"] == False:
                tasks[taskId]=db[taskId]
        return tasks
    else:
        return db

@app.delete("/tarefas/{uuid}", tags=["Tarefas"], name="Deletar tarefa", description="Exclui uma tarefa da lista de tarefas")
async def delete_tarefa(idT: str):
    '''
    Remove uma tarefa a partir de um id
    '''
    if idT in db:
        if idT in db:
            del db[idT]
            return idT
    else:
        raise HTTPException(status_code=404, detail="Não foi possível excluir esta tarefa...")
        return

@app.patch("/tarefas/{uuid}", tags=["Tarefas"], name="Editar tarefa", description="Permite editar status e descrição da tarefa")
async def update_status(idT: str, editedTask: Tarefa):
    '''
    Atualiza uma tarefa de id igual ao parametro idT
    '''
    if idT in db:
        storedTaskData = db[idT]
        storedTaskModel = Tarefa(**storedTaskData)
        updateTask = editedTask.dict(exclude_unset=True)
        updatedTask = storedTaskModel.copy(update=updateTask)
        db[idT] = jsonable_encoder(updatedTask)
        return updatedTask
    else: 
        raise HTTPException(status_code=404, detail="Não conseguimos encontrar esta tarefa...")
        return
