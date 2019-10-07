import json

def load_json(file):
    with open(file) as f:
        return json.load(f)


def get_students():
    return load_json('db.json')['alumnos']


def get_student(student_id):
    return get_students()[student_id]


def insert_student(student):
    students = get_students()
    students.update(student)
    return students


def delete_student(student_id):
    students = get_students()
    del students[student_id]
    return students


def update_student(student_id, field, value):
    students = get_students()
    students[student_id][field] = value
    return students
