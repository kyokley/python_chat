from db import (Table,
                IntegerColumn,
                TextColumn,
                )


class Student(Table):
    TABLE_NAME = 'student'

    id = IntegerColumn('id', primary_key=True)
    first_name = TextColumn('first_name')
    last_name = TextColumn('last_name')
    grade = IntegerColumn('grade')

    @property
    def scores(self):
        from score import Score
        self._db.execute('''
            SELECT id, student_id, score, subject FROM score
            WHERE student_id = ?
        ''', (self.id,))
        rows = self._db.fetchall()
        return [Score(self,
                      row[2],
                      row[3],
                      id=row[0],
                      save=False)
                for row in rows]

    def __init__(self, first_name, last_name, grade, id=None, save=True):
        self.id = id or self.get_next_id()
        self.first_name = first_name
        self.last_name = last_name
        self.grade = grade

        if save:
            self.save()

    def __str__(self):
        return f'<{self.__class__.__name__}: id={self.id} {self.first_name} {self.last_name} {self.grade}>'

    @classmethod
    def get(cls, id):
        cls._db.execute('''
            SELECT id, first_name, last_name, grade from student where id = ?
        ''', (id,))
        row = cls._db.fetchone()
        return cls(row[1],
                   row[2],
                   row[3],
                   id=row[0],
                   save=False)

    @classmethod
    def all(cls):
        cls._db.execute('''
            SELECT id, first_name, last_name, grade from student
        ''')
        rows = cls._db.fetchall()
        return [cls(row[1],
                    row[2],
                    row[3],
                    id=row[0],
                    save=False)
                for row in rows]
