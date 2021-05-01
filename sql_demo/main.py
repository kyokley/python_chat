import random
from faker import Faker
from student import Student
from score import Score, Subject
from db import Database


rand = random.SystemRandom()
NUMBER_OF_STUDENTS = 10000
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
        print(f'Created {NUMBER_OF_STUDENTS} new records')
        total = Student.count()
        print(f'{total} Student records total')

        Score.create_table()
        for student in students:
            mean = rand.random() * 100 + 1
            for i in range(NUMBER_OF_SCORES):
                Score(student,
                      int(max(min((rand.random() - .5) * 50 + mean, 100), 50)),
                      rand.choice(list(Subject)))
        print(f'Created {NUMBER_OF_STUDENTS * NUMBER_OF_SCORES} new records')
        total = Score.count()
        print(f'{total} Score records total')


def refresh():
    student = Student.get(53)
    student.first_name = 'asdf'
    student.refresh_from_db()


if __name__ == '__main__':
    main()
    # refresh()
