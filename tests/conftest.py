import json
from pytest import fixture
from app import app as server

@fixture
def app():
    return server

@fixture
def valid_student():
    with open('data/sample.json') as f:
        return json.dumps(json.load(f))