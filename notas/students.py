import json
import fastjsonschema
from functools import wraps
from flask import Flask, request
from flask_restplus import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

with open('schema.json') as file:
    validate = fastjsonschema.compile(json.load(file))

STUDENTS = {}

def abort_invalid_student(func):
    @wraps(func)
    def wrapper(self, student_id, *args, **kwargs):
        if student_id in STUDENTS:
            return func(self, student_id, *args, **kwargs)
        else:
            abort(404, message=f"The student {student_id} doesnt exist")
    return wrapper

@api.route('/students')
class StudentsList(Resource):
    def get(self):
        return STUDENTS
    
    def post(self):
        body = request.get_json()
        student_id = next(iter(body))
        data = body[student_id]

        try:
            validate(data)
        except fastjsonschema.JsonSchemaException as e:
            abort(404, message=e.message)

        STUDENTS[student_id] = data
        return {'message' : 'Student added succesfully!'}

@api.route('/students/<student_id>')
class Student(Resource):
    @abort_invalid_student
    def get(self, student_id):
        return STUDENTS[student_id]

    @abort_invalid_student
    def delete(self, student_id):
        del STUDENTS[student_id]
        return '', 204

    @abort_invalid_student
    def put(self, student_id):
        STUDENTS[student_id] = student_id
        return student_id, 201


if __name__ == '__main__':
    app.run(debug=True)