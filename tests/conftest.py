import json
from pytest import fixture
import notas.app as server

@fixture
def app():
    app = server.app
    return app

@fixture
def valid_student():
    with open('data/sample.json') as f:
        return json.dumps(json.load(f))