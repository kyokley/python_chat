from db import (Table,
                IntegerColumn,
                TextColumn,
                ForeignKey,
                )
from utils import StrEnum
from student import Student


class Subject(StrEnum):
    MATH = 'math'
    SCIENCE = 'science'
    LITERATURE = 'literature'
    SOCIAL_STUDIES = 'social studies'


class Score(Table):
    TABLE_NAME = 'score'
    pk = IntegerColumn('pk', primary_key=True)
    student = ForeignKey(Student)
    score = IntegerColumn('score')
    subject = TextColumn('subject')

    def __init__(self, student, score, subject, pk=None, save=True):
        self.pk = pk or self._db.get_id()
        self.student = student
        self.score = score
        self.subject = subject

        if save:
            self.save()

    def _get_subject(self):
        return self._subject

    def _set_subject(self, val):
        if not isinstance(val, Subject):
            val = Subject.from_string(val)
        self._subject = val

    def __str__(self):
        return f'<{self.__class__.__name__}: pk={self.pk} {self.student.first_name} {self.student.last_name} {self.score} {self.subject}>'
