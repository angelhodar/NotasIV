import pytest
import json

@pytest.mark.order1
def test_get_students(client):
    response = client.get("/api/v1/students")
    assert response.status_code == 200
    assert response.json == {'data': []}


@pytest.mark.order2
def test_post_student(client, valid_student):
    response = client.post("/api/v1/students", data=valid_student, content_type='application/json')
    assert response.status_code == 201
    response = client.post("/api/v1/students", data='{}', content_type='application/json')
    assert response.status_code == 400


@pytest.mark.order3
def test_get_student(client, valid_student):
    response = client.get("/api/v1/students/1")
    assert response.status_code == 200
    assert response.json['github'] == json.loads(valid_student)['github']
    response = client.get("/api/v1/students/fail")
    assert response.status_code == 404


@pytest.mark.order4
def test_put_student(client, valid_student):
    response = client.put("/api/v1/students/1", data=valid_student, content_type='application/json')
    assert response.status_code == 204
    response = client.put("/api/v1/students/fail")
    assert response.status_code == 404
    response = client.post("/api/v1/students", data='{}', content_type='application/json')
    assert response.status_code == 400


@pytest.mark.order5
def test_delete_student(client):
    response = client.delete("/api/v1/students/1")
    assert response.status_code == 204
    response = client.delete("/api/v1/students/fail")
    assert response.status_code == 404


