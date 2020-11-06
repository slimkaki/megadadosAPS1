from fastapi.testclient import TestClient
from .main import app
import json, uuid
from .models import Task

client = TestClient(app)

uuids = []
completed_tasks_uuids = []
incompleted_tasks_uuids = []



#--------- GET ROOT ------------#
def test_read_main_returns_not_found():
    """
    Teste: teste padrão do /
    Verbo: GET
    """
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

#--------- POST ÚNICO ----------#
def test_post_valid_task():
    """
    Teste: Realizar o POST de uma task e verificar se foi bem-sucedida. 
           O UUID é guardado na lista "uuids" para os próximos testes.
    Verbo: POST
    """
    data = json.dumps({
        "description": "Primeiro Teste",
        "completed": False
        })
    response = client.post('/task', data)
    uuids.append(response.json())
    assert response.status_code == 200


#--------- GET ÚNICO ----------#
def test_get_single_task():
    """
    Teste: Busca de uma task a partir de um UUID conhecido.
    Verbo: GET
    Esperado: Status Code = 200
    """
    url = "/task/" + str(uuids[0])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {
        "description": "Primeiro Teste",
        "completed": False
    }

# ------ POPULAR A BASE PARA TESTES -----#
def test_post_tasks_200():
    """
    Teste: Realizar o POST de algumas tasks e verificar se são bem-sucedidas. 
           Os UUID's são guardados para os próximos testes.
    Verbo: POST
    """
    for i in range(3):
        data = json.dumps({
            "description": f"meu Teste {i}",
            "completed": False
            })
        response = client.post('/task', data)
        uuids.append(response.json())

        assert response.status_code == 200


#------ TEST VALID DELETE -------#
def test_delete_task():
    """
    Teste: Deletar uma task de UUID conhecido.
    Verbo: DELETE
    Esperado: Status Code = 200
    """
    response = client.delete('/task/' + uuids[0])
    assert response.status_code == 200
    get_all_tasks = client.get('/task')
    assert len(get_all_tasks.json()) == len(uuids)-1
    uuids.remove(uuids[0])

#------ TEST DELETE UNKNOWN TASK-------#
def test_delete_invalid_task():
    """
    Teste: Deletar uma task com um UUID aleatório.
    Verbo: DELETE
    Esperado: Status Code = 404
    """
    response = client.delete('/task/' + str(uuid.uuid4()))
    assert response.status_code == 404

# ----- POST OBJETO INCOMPLETO ---------#
def test_post_task_no_info():
    """
    Teste: POST com payload vazio. funciona pois cria com default
    Verbo: POST 
    Esperado: Deveria funcionar, pois cria com "description" e "completed" default.
    """
    data = json.dumps({})
    response = client.post('/task', data)
    uuids.append(response.json())
    created_task = client.get('/task/' + str(uuids[-1]))
    assert created_task.json() == {"description": "no description", "completed": False}



#------- POST INFOS DESNECESSÁRIAS PARA A REQ ----#
def test_post_task_additional_info():
    """
    Teste: POST com payload com chaves aleatórias para o json.
    Verbo: POST
    Esperado: Deveria funcionar, pois cria com "description" e "completed" default.
    """
    data = json.dumps({
        "maca": "Teste",
        "banana": False
        })
    response = client.post('/task', data)
    uuids.append(response.json())
    created_task = client.get('/task/' + str(uuids[-1]))
    assert created_task.json() == {"description": "no description", "completed": False}

#------- GET ALL TASKS -------#
def test_get_all():
    """
    Teste: Retorna todos os objetos no db.
    Verbo: GET
    Esperado: Status Code 200 e todos os objetos no db também se encontram na lista "uuids".
    """
    response = client.get('/task')
    assert response.status_code == 200
    for j in response.json():
        if j in uuids:
            assert True
        else:
            assert False


#------- GET UNKOWN TASK -------#
def test_get_single_task_wrong_uuid():
    """
    Teste: Retorna uma task só, porém é passado um UUID aleatório
    Verbo: GET
    Esperado: Status Code = 404
    """
    url = "/task/" + str(uuid.UUID)
    response = client.get(url)
    assert response.status_code == 422

#------ PUT VALID TASK (REPLACE WHOLE TASK) ------#
def test_put_with_valid_uuid():
    """
    Teste: Substitui uma task inteira com uuid conhecido
    Verbo: PUT
    Esperado: Status Code = 200
    """
    url = "/task/" + str(uuids[0])
    completed_tasks_uuids.append(uuids[0])
    data = json.dumps({
        "description": "Replaced Whole Task",
        "completed": True
    })
    response = client.put(url, data)
    assert response.status_code == 200
    replaced_task = client.get('/task/' + str(uuids[0]))
    assert replaced_task.json() == {
        "description": "Replaced Whole Task",
        "completed": True
    }

#------- PUT EM TASK INEXISTENTE -------#
def test_put_with_invalid_uuid():
    """
    Teste: Substitui uma task inteira com uuid desconhecido
    Verbo: PUT
    Esperado: Status Code = 200
    """
    scoped_uuid = str(uuid.uuid4())
    url = "/task/" + scoped_uuid
    data = json.dumps({
        "description": "PUT Created task from nothing",
        "completed": True
    })
    completed_tasks_uuids.append(scoped_uuid)
    response = client.put(url, data)
    assert response.status_code == 200
    created_with_put_task = client.get(url)
    assert created_with_put_task.json() == {
        "description": "PUT Created task from nothing",
        "completed": True
    }

#----- PATCH VALID UUID ----------#
def test_patch_with_valid_uuid():
    """
    Teste: Atualiza os dados de uma task de uuid conhecido.
    Verbo: PATCH
    Esperado: Status Code = 200
    """
    url = "/task/" + str(uuids[1])
    data = json.dumps({
        "description": "Updated Task",
        "completed": True
    })
    completed_tasks_uuids.append(uuids[1])
    response = client.patch(url, data)
    assert response.status_code == 200
    assert response.json() == None
    updated_task = client.get('/task/' + str(uuids[1]))
    assert updated_task.json() == {
        "description": "Updated Task",
        "completed": True
    }

#----- PATCH INVALID UUID ----------#
def test_patch_unknown_task():
    """
    Teste: Atualiza os dados de uma task com uuid aleatório.
    Verbo: PATCH
    Esperado: Status Code = 404
    """
    url = "/task/" + str(uuid.uuid4())
    data = json.dumps({
    "description": "Updated Task",
    "completed": True
    })
    response = client.patch(url, data)
    assert response.status_code == 404



#------- GET ALL COMPLETED TASKS -------#
def test_get_all_completed():
    """
    Teste: GET SOMENTE AS TASKS COMPLETAS
    Verbo: GET
    Esperado: Que todos os objetos retornados na response tenham seus uuid's salvos na lista
              "completed_tasks_uuids".
    """
    response = client.get('/task?completed=true')
    assert response.status_code == 200
    for j in response.json():
        if j in completed_tasks_uuids:
            assert True
        else:
            assert False


#------- GET ALL INCOMPLETED TASKS -------#
def test_get_all_incompleted():
    """
    Teste: GET SOMENTE AS TASKS INCOMPLETAS
    Verbo: GET
    Esperado: Que todos os objetos retornados na response tenham seus uuid's salvos na lista
              "incompleted_tasks_uuids".
    """
    incompleted_tasks_uuids = uuids
    for i in completed_tasks_uuids:
        if i in incompleted_tasks_uuids:
            incompleted_tasks_uuids.remove(i)

    response = client.get('/task?completed=false')
    assert response.status_code == 200
    for j in response.json():
        if j in incompleted_tasks_uuids:
            assert True
        else:
            assert False
