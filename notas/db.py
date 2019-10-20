from tinydb import TinyDB
from tinydb.storages import MemoryStorage


db = TinyDB(storage=MemoryStorage)


def get_student(student_id):
    return db.get(doc_id=student_id)


def get_students():
    return db.all()


def add_student(student):
    student_id = db.insert(student)
    return student_id


def remove_student(student_id):
    ids = db.remove(doc_ids=[student_id])
    return student_id in ids


def update_student(student_id, new_data):
    ids = db.update(new_data, doc_ids=[student_id])
    return student_id in ids