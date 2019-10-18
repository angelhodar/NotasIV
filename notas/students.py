from flask import Flask, request
from flask_restplus import Api, Resource, abort, fields

app = Flask(__name__)
api = Api(app)

STUDENTS = {}

def abort_student(student_id):
    abort(404, message=f"The student {student_id} doesnt exist")


class Student(Resource):
    def get(self, student_id):
        if student_id not in STUDENTS:
            abort_student(student_id)
        return STUDENTS[student_id]

    def delete(self, student_id):
        if student_id not in STUDENTS:
            abort_student(student_id)
        del STUDENTS[student_id]
        return '', 204

    def put(self, student_id):
        if student_id not in STUDENTS:
            abort_student(student_id)
        STUDENTS[student_id] = student_id
        return student_id, 201


class StudentsList(Resource):
    def get(self):
        return STUDENTS

    def post(self):
        student_data = request.get_json()
        student_id = next(iter(student_data))
        STUDENTS[student_id] = student_data
        return {'message' : 'Student added succesfully!'}


# Routing
api.add_resource(StudentsList, '/students')
api.add_resource(Student, '/students/<student_id>')


if __name__ == '__main__':
    app.run(debug=True)