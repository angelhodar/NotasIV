from notas import db
from flask import Flask, request
from flask_restplus import Api, Resource, abort, fields
from notas.utils import abort_invalid_student, get_schema

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="NotasIV API",
    description="API para el microservicio de la asignatura Infraestructura Virtual (2019-2020)"
)

status_ns = api.namespace('Status', path="/")
students_ns = api.namespace("NotasIV", path="/api/v1")

student_schema = api.schema_model('Student Schema', get_schema())
student_list_schema = api.model('Students List Schema', {
    'data': fields.List(fields.Nested(student_schema))
})
check_status = api.model('Status', {
    'status': fields.String(default="OK")
})

@status_ns.route('/status')
class CheckStatus(Resource):
    @api.response(200, 'Success', check_status)
    def get(self):
        return {'status': "OK"}

@students_ns.route("/students")
class StudentsList(Resource):
    @api.response(200, 'Success', student_list_schema)
    def get(self):
        return {'data': db.get_students()}

    @api.response(201, 'Student created')
    @api.response(400, 'Validation Error')
    @api.expect(student_schema, validate=True)
    def post(self):
        data = request.get_json()
        student_id = db.add_student(data)
        return student_id, 201


@students_ns.route("/students/<int:student_id>")
@api.doc(params={"student_id": "Student's resource id"})
class Student(Resource):
    @api.response(200, 'Success"', student_schema)
    @api.response(404, 'Student not found')
    @abort_invalid_student
    def get(self, student_id):
        return db.get_student(student_id)

    @api.response(204, 'Student deleted')
    @api.response(404, 'Student not found')
    @abort_invalid_student
    def delete(self, student_id):
        db.remove_student(student_id)
        return '', 204

    @api.response(204, 'Student updated')
    @api.response(400, 'Validation error')
    @api.response(404, 'Student not found')
    @api.expect(student_schema, validate=True)
    @abort_invalid_student
    def put(self, student_id):
        data = request.get_json()
        db.update_student(student_id, data)
        return '', 204


if __name__ == "__main__":
    app.run(debug=True)
