import json
from pytest import fixture
from notas.utils import get_json
from app import app as server

@fixture
def app():
    return server

@fixture
def valid_student():
    return json.dumps(get_json('sample.json'))

@fixture
def status():
    return get_json('status.json')