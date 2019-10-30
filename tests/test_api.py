import pytest
import json

@pytest.mark.order1
def test_status(client):
    """Testea si se recibe código 200 en la ruta /status
    con una petición GET y que el resultado sea un JSON con formato
    {'status': "OK"}
    
    Args:
        client (Flask.test_client): Mock de la API para mandar peticiones durante los tests.
    """
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json == {'status': "OK"}


@pytest.mark.order2
def test_get_students(client):
    """Testea si se recibe código 200 en la ruta /api/v1/students
    con una petición GET y que el resultado sea una lista vacía ya que
    no hay datos previamente cargados.
    
    Args:
        client (Flask.test_client): Mock de la API para mandar peticiones durante los tests.
    """
    response = client.get("/api/v1/students")
    assert response.status_code == 200
    assert response.json == {'data': []}


@pytest.mark.order3
def test_post_student(client, valid_student):
    """Testea si se recibe código 201 en la ruta /api/v1/students
    con una petición POST al mandar un esquema de estudiante válido
    o 400 si no es válido (en este caso se envía un json vacío).
    
    Args:
        client (Flask.test_client): Mock de la API para mandar peticiones durante los tests.
        valid_student (dict): JSON con una estructura de estudiante válida.
    """
    response = client.post("/api/v1/students", data=valid_student, content_type='application/json')
    assert response.status_code == 201
    response = client.post("/api/v1/students", data='{}', content_type='application/json')
    assert response.status_code == 400


@pytest.mark.order4
def test_get_student(client, valid_student):
    """Testea si se recibe código 200 en la ruta /api/v1/students/<student_id>
    con una petición GET al mandar un identificador de estudiante válido a la vez que
    comprueba que el JSON recibido sea adecuado, o 404 si el identificador de estudiante
    no es válido.
    
    Args:
        client (Flask.test_client): Mock de la API para mandar peticiones durante los tests.
        valid_student (dict): JSON con una estructura de estudiante válida.
    """
    response = client.get("/api/v1/students/1")
    assert response.status_code == 200
    assert response.json['github'] == json.loads(valid_student)['github']
    response = client.get("/api/v1/students/fail")
    assert response.status_code == 404


@pytest.mark.order5
def test_put_student(client, valid_student):
    """Testea si se recibe código 204 en la ruta /api/v1/students/<student_id>
    con una petición PUT al mandar un esquema e identificador de estudiante válido.
    Si no se encuentra el estudiante comprueba si devuelve 404, o 400 si el esquema
    no es válido (en este caso se envía un json vacío).
    
    Args:
        client (Flask.test_client): Mock de la API para mandar peticiones durante los tests.
        valid_student (dict): JSON con una estructura de estudiante válida.
    """
    response = client.put("/api/v1/students/1", data=valid_student, content_type='application/json')
    assert response.status_code == 204
    response = client.put("/api/v1/students/fail")
    assert response.status_code == 404
    response = client.post("/api/v1/students", data='{}', content_type='application/json')
    assert response.status_code == 400


@pytest.mark.order6
def test_delete_student(client):
    """Testea si se recibe código 204 en la ruta /api/v1/students/<student_id>
    con una petición DELETE al mandar un identificador de estudiante válido, o 404
    si no existe ese identificador.
    
    Args:
        client (Flask.test_client): Mock de la API para mandar peticiones durante los tests.
    """
    response = client.delete("/api/v1/students/1")
    assert response.status_code == 204
    response = client.delete("/api/v1/students/fail")
    assert response.status_code == 404


