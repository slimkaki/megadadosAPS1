from fastapi.testclient import TestClient
from main import app
import json, uuid

client = TestClient(app)

uuids = []

def test_read_main_returns_not_found():
    """
    Teste: teste padrão do /
    Verbo: GET
    """
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_post_tasks_200():
    """
    Teste: Realizar o POST de algumas tasks e verificar se são bem-sucedidas. 
           Os UUID's são guardados para os próximos testes.
    Verbo: POST
    """
    for i in range(3):
        data = json.dumps({
            "description": f"meu Teste {i}",
            "completed": "false"
            })
        response = client.post('/task', data)
        uuids.append(response.json())

        assert response.status_code == 200

def test_post_tasks_404():
    """
    Teste: Realizar 
    Verbo: POST 
    """
    for i in range(3):
        data = json.dumps({
            "maca": f"Teste {i}",
            "banana": "false"
            })
        response = client.post('/task', data)
        uuids.append(response.json())
        assert response.status_code == 404

def test_get_all():
    """
    Teste:
    Verbo: GET
    Saída esperada:
    """
    response = client.get('/task')
    assert response.status_code == 200
    for j in response.json():
        if j in uuids:
            assert True
        else:
            assert False

def test_get_single_task():
    """
    Teste: retorna uma task só. É passado um UUID conhecido
    Verbo: GET
    Esperado: Status Code = 200
    """
    url = "/task/" + str(uuids[0])
    response = client.get(url)
    assert response.status_code == 200

def test_get_single_task_wrong_uuid():
    """
    Teste: retorna uma task só, porém é passado um UUID aleatório
    Verbo: GET
    Esperado: Status Code = 404
    """
    url = "/task/" + str(uuid.UUID)
    response = client.get(url)
    assert response.status_code == 422

# def test_put_replace():