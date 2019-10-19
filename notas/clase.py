import json

def load_json(file):
    with open(file) as f:
        return json.load(f)


def get_students():
    """Returns all the stored students
    
    Returns:
        (list): Dict of students
    """
    return load_json('data/samples.json')['alumnos']


def get_student(student_id):
    """Returns a student by its given id
    
    Args:
        student_id (str): The github username of the student
    
    Returns:
        (dict): Student data
    """
    for student in get_students():
        if student['github'] == student_id:
            return student


def insert_student(student):
    """Inserts a new student
    
    Args:
        student (dict): Student data.
    
    Returns:
        (dict): All students with the new one inserted.
    """
    students = get_students()
    students.append(student)
    return students


def delete_student(student_id):
    """Removes a student
    
    Args:
        student_id (str): The github username of the student.
    
    Returns:
        (dict): All students without the deleted one
    """
    students = get_students()
    for i, student in enumerate(students):
        if student['github'] == student_id:
            del students[i]
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
    for student in students:
        if student['github'] == student_id:
            student[field] = value
    return students
