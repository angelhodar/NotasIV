import json
import api_db as db
from functools import wraps
from flask_restplus import abort

def get_schema():
    with open("schema.json") as file:
        return json.load(file)

def abort_invalid_student(func):
    @wraps(func)
    def wrapper(self, student_id, *args, **kwargs):
        if db.get_student(student_id):
            return func(self, student_id, *args, **kwargs)
        else:
            abort(400, message=f"The student {student_id} doesnt exist")
    return wrapper