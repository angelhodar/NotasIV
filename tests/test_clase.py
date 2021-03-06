from notas import clase as db

def test_student_get():
    student = db.get_student('angelhodar')
    assert student is not None
    assert isinstance(student, dict)


def test_student_insert():
    students = db.get_students()
    new_student = db.load_json('data/sample.json')

    # Check the actual count of students and the id of inserted one
    count = len(students)
    student_id = new_student['github']
    
    # Insert a new student
    students = db.insert_student(new_student)

    # Checks that the student has been inserted
    assert len(students) == count + 1
    assert student_id in [s['github'] for s in students]


def test_student_delete():
    students = db.get_students()

    count = len(students)
    student_id = 'angelhodar'

    students = db.delete_student(student_id)

    assert len(students) != count
    assert student_id not in [s['github'] for s in students]


def test_student_update():
    students = db.get_students()

    student_id = 'angelhodar'
    field = 'nombre'
    value = 'Ivan'

    old_value = students[0][field]
    students = db.update_student(student_id, field, value)
    new_value = students[0][field]

    assert new_value != old_value
    assert new_value == value