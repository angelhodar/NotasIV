import json
from notas import db
from functools import wraps
from flask_restplus import abort

def get_json(filename):
    with open("data/{}".format(filename)) as file:
        return json.load(file)

def abort_invalid_student(func):
    @wraps(func)
    def wrapper(self, student_id, *args, **kwargs):
        if db.get_student(student_id):
            return func(self, student_id, *args, **kwargs)
        else:
            abort(400, message="The student {} doesnt exist".format(student_id))
    return wrapper