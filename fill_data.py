from string import ascii_uppercase
import faker
from random import randint
import sqlite3

NUMBER_STUDENTS = 250
NUMBER_GROUPS = 10
NUMBER_SUBJECTS = 6
NUMBER_TEACHERS = 8
NUMBER_GRADES = 20
SUBJECTS = [
    "Mathematics",
    "Biology",
    "Chemistry",
    "History",
    "Literature",
    "Physics",
    "Psychology",
    "Computer Science",
]

GRADES = [1, 2, 3, 4, 5]
PROBABILITIES = [1, 5, 15, 45, 34]

INSERT_GROUP_QUERY = "INSERT INTO groups(group_name) VALUES (?)"
INSERT_STUDENT_QUERY = "INSERT INTO students(student, group_id) VALUES (?, ?)"
INSERT_SUBJECT_QUERY = "INSERT INTO subjects(subject_name) VALUES (?)"
INSERT_TEACHER_QUERY = "INSERT INTO teachers(teacher, subject_id) VALUES (?, ?)"
INSERT_GRADE_QUERY = "INSERT INTO journal(student_id, subject_id, grade, grade_date) VALUES (?, ?, ?, ?)"


def get_random_grade():
    rand_num = randint(1, 100)
    cumulative_prob = 0
    for i, prob in enumerate(PROBABILITIES):
        cumulative_prob += prob
        if rand_num <= cumulative_prob:
            return GRADES[i]


def insert_data_to_db(students, groups, subjects, teachers, journal) -> None:
    with sqlite3.connect("student_journal.db") as con:
        cur = con.cursor()
        cur.executemany(INSERT_GROUP_QUERY, groups)
        cur.executemany(INSERT_STUDENT_QUERY, students)
        cur.executemany(INSERT_SUBJECT_QUERY, subjects)
        cur.executemany(INSERT_TEACHER_QUERY, teachers)
        cur.executemany(INSERT_GRADE_QUERY, journal)
        con.commit()


def generate_fake_data(number_students, number_groups, number_subjects, number_teachers, number_grades):
    fake_students = []
    fake_groups = []
    fake_teachers = []
    fake_journal = []
    fake_subjects = []

    fake_data = faker.Faker()

    generated_names = set()

    for _ in range(number_students):
        student_name = fake_data.name()
        while student_name in generated_names:
            student_name = fake_data.name()
        generated_names.add(student_name)
        fake_students.append((student_name, randint(1, number_groups)))

    for _ in range(number_groups):
        fake_groups.append((fake_data.bothify(text="??-##", letters=ascii_uppercase),))

    for _ in range(number_teachers):
        fake_teachers.append((fake_data.name(), randint(1, number_subjects)))

    for student_id in range(1, number_students + 1):
        for subject_id in range(1, number_subjects + 1):
            for _ in range(randint(10, number_grades + 1)):
                fake_journal.append((student_id, subject_id, get_random_grade(), fake_data.date_this_year()))

    for subject in SUBJECTS:
        fake_subjects.append((subject,))

    return fake_students, fake_groups, fake_subjects, fake_teachers, fake_journal


if __name__ == "__main__":
    students, groups, subjects, teachers, journal = generate_fake_data(
        NUMBER_STUDENTS, NUMBER_GROUPS, NUMBER_SUBJECTS, NUMBER_TEACHERS, NUMBER_GRADES
    )

    insert_data_to_db(students, groups, subjects, teachers, journal)
