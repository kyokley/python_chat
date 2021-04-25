import random
from faker import Faker
from student import Student
from score import Score, Subject
from db import Database


NUMBER_OF_STUDENTS = 1000
NUMBER_OF_SCORES = 100
fake = Faker()


def main():
    db = Database()

    with db.connection:
        Student.create_table()
        students = [Student(fake.first_name(),
                            fake.last_name(),
                            random.randint(1, 12))
                    for i in range(NUMBER_OF_STUDENTS)]

        Score.create_table()
        for student in students:
            for i in range(NUMBER_OF_SCORES):
                Score(student, random.randint(50, 100), random.choice(list(Subject)))


def refresh():
    import pdb; pdb.set_trace()  # ############################## Breakpoint ##############################
    student = Student.get(53)
    student.first_name = 'asdf'
    student.refresh_from_db()


if __name__ == '__main__':
    # main()
    refresh()
