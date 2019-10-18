import json
import fastjsonschema
from functools import wraps
from flask import Flask, request
from flask_restplus import Api, Resource, abort

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="NotasIV API",
    description="API para el microservicio de la asignatura Infraestructura Virtual en el curso 2019-2020",
)

namespace = api.namespace("NotasIV", path="/")

with open("schema.json") as file:
    validate = fastjsonschema.compile(json.load(file))

STUDENTS = {}


def abort_invalid_student(func):
    @wraps(func)
    def wrapper(self, student_id, *args, **kwargs):
        if student_id in STUDENTS:
            return func(self, student_id, *args, **kwargs)
        else:
            abort(400, message=f"The student {student_id} doesnt exist")

    return wrapper


@namespace.route("/students")
class StudentsList(Resource):
    @api.doc(responses={200: "Success"})
    def get(self):
        return STUDENTS

    @api.doc(responses={201: "Success", 400: "Validation Error"})
    def post(self):
        data = request.get_json()
        try:
            student_id = next(iter(data))
            data = data[student_id]
            validate(data)
            STUDENTS[student_id] = data
            return {"message": "Student added succesfully!"}
        except TypeError as e:
            abort(400, message="No data specified in body")
        except KeyError as e:
            abort(400, message="No student id specified")
        except fastjsonschema.JsonSchemaException as e:
            abort(400, message=e.message)


@namespace.route("/students/<student_id>")
@api.doc(params={"student_id": "Usuario de github del estudiante"})
class Student(Resource):
    @api.doc(responses={200: "Success", 404: "Student not found"})
    @abort_invalid_student
    def get(self, student_id):
        return STUDENTS[student_id]

    @api.doc(responses={204: "Success", 404: "Student not found"})
    @abort_invalid_student
    def delete(self, student_id):
        del STUDENTS[student_id]
        return "", 204

    @api.doc(responses={204: "Success", 404: "Student not found", 400: "Validation Error"})
    @abort_invalid_student
    def put(self, student_id):
        data = request.get_json()
        data = {} if not data else data
        try:
            validate(data)
            STUDENTS[student_id] = data
            return '', 204
        except fastjsonschema.JsonSchemaException as e:
            abort(400, message=e.message)


if __name__ == "__main__":
    app.run(debug=True)
