import json

def load_json(file):
    with open(file) as f:
        return json.load(f)


def get_students():
    """Returns all the stored students
    
    Returns:
        (list): Dict of students
    """
    return load_json('db.json')['alumnos']


def get_student(student_id):
    """Returns a student by its given id
    
    Args:
        student_id (str): The github username of the student
    
    Returns:
        (dict): Student data
    """
    return get_students()[student_id]


def insert_student(student):
    """Inserts a new student
    
    Args:
        student (dict): Student data.
    
    Returns:
        (dict): All students with the new one inserted.
    """
    students = get_students()
    students.update(student)
    return students


def delete_student(student_id):
    """Removes a student
    
    Args:
        student_id (str): The github username of the student.
    
    Returns:
        (dict): All students without the deleted one
    """
    students = get_students()
    del students[student_id]
    return students


def update_student(student_id, field, value):
    """Returns a student by its given id
    
    Args:
        student_id (str): The github username of the student.
        field (str): The field to update.
        value (str): The new value for the field.
    
    Returns:
        (dict): All students with the selected one updated.
    """
    students = get_students()
    students[student_id][field] = value
    return students
