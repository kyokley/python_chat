import sqlite3
from itertools import chain
from pathlib import Path
from utils import StrEnum


DATABASE_PATH = Path('example.db')


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.db_path = DATABASE_PATH
        self._connection = None
        self._cursor = None
        self._max_id = self._set_max_id()

    def _set_max_id(self):
        try:
            query = '''select max(pk) from student'''
            self.cursor.execute(query)
            max_val = self.cursor.fetchone()[0] or 0
        except sqlite3.OperationalError:
            max_val = 0

        try:
            query = '''select max(pk) from score'''
            self.cursor.execute(query)
            max_val = max(max_val, self.cursor.fetchone()[0] or 0)
        except sqlite3.OperationalError:
            pass

        return max_val + 1

    def get_id(self):
        self._max_id += 1
        return self._max_id

    @property
    def connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(DATABASE_PATH)
        return self._connection

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def commit(self):
        self.connection.commit()
        self._cursor = None

    def rollback(self):
        self.connection.rollback()
        self._cursor = None


class ColumnType(StrEnum):
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    FOREIGN_KEY = 'FOREIGN_KEY'


class Column:
    def __init__(self, name, col_type, db_column=None, null=False, primary_key=False):
        self.name = name
        self.col_type = col_type
        self.null = null
        self.primary_key = primary_key

        if db_column is None:
            db_column = self.name
        self.db_column = db_column

    @property
    def creation_statement(self):
        return f'{self.db_column} {self.col_type} {"NOT NULL" if not self.null else ""} {"PRIMARY KEY" if self.primary_key else ""}'

    @property
    def foreign_key_statement(self):
        return None

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}>'


class IntegerColumn(Column):
    def __init__(self, name, db_column=None, null=False, primary_key=False):
        super().__init__(name,
                         ColumnType.INTEGER,
                         db_column=db_column,
                         null=null,
                         primary_key=primary_key)


class TextColumn(Column):
    def __init__(self, name, db_column=None, null=False, primary_key=False):
        super().__init__(name,
                         ColumnType.TEXT,
                         db_column=db_column,
                         null=null,
                         primary_key=primary_key)


class ForeignKey(Column):
    def __init__(self, klass, null=False):
        self.klass = klass
        name = self.klass.TABLE_NAME
        db_column = f'{name}_id'
        primary_key = False

        super().__init__(name,
                         ColumnType.FOREIGN_KEY,
                         db_column=db_column,
                         null=null,
                         primary_key=primary_key)

    @property
    def creation_statement(self):
        return f'''{self.db_column} {ColumnType.INTEGER} {"NOT NULL" if not self.null else ""} {"PRIMARY KEY" if self.primary_key else ""}
        '''

    @property
    def foreign_key_statement(self):
        return f'''FOREIGN KEY ({self.db_column}) REFERENCES {self.klass.TABLE_NAME} ({self.klass.primary_key_column().db_column})
               ON DELETE CASCADE ON UPDATE NO ACTION
            '''


class Table:
    TABLE_NAME = None
    _initialized = False
    _db = Database()

    @classmethod
    def primary_key_column(cls):
        for col in cls.mapped_columns():
            if col.primary_key:
                return col
        raise Exception('No primary key has been defined')

    @classmethod
    def mapped_columns(cls):
        return [v for k, v in cls.__dict__.items() if isinstance(v, Column)]

    @classmethod
    def create_table(cls):
        try:
            column_definitions = ', '.join(
                chain(
                    [col.creation_statement for col in cls.mapped_columns()],
                    [col.foreign_key_statement for col in cls.mapped_columns() if col.foreign_key_statement]
                )
            )
            query = f'''
                CREATE TABLE {cls.TABLE_NAME}
                    ({column_definitions});
            '''
            cls._db.execute(query)
            cls._db.commit()
        except sqlite3.OperationalError:
            pass
        finally:
            cls._initialized = True

    def save(self):
        exists_query = f'''
            SELECT 1 FROM {self.TABLE_NAME}
            WHERE pk = {self.pk}
        '''
        self._db.execute(exists_query)
        exists = self._db.fetchone()

        if not exists:
            values = tuple(
                [getattr(self, col.name) if col.col_type != ColumnType.FOREIGN_KEY
                 else getattr(getattr(self, col.name), getattr(self, col.name).primary_key_column().name)
                 for col in self.mapped_columns()]
            )

            self._db.execute(f'''
                INSERT INTO {self.TABLE_NAME}
                ({', '.join([col.db_column for col in self.mapped_columns()])})
                VALUES ({', '.join(['?' for i in range(len(self.mapped_columns()))])})
            ''', values)
        else:
            values = tuple(
                [getattr(self, col.name) if col.col_type != ColumnType.FOREIGN_KEY
                 else getattr(getattr(self, col.name), getattr(self, col.name).primary_key_column().name)
                 for col in self.mapped_columns()
                 if not col.primary_key
                 ]
            )
            values += (getattr(self, self.primary_key_column().name),)
            set_statement = ', '.join([
                f'{col.name} = ?'
                for col in self.mapped_columns()
                if not col.primary_key
            ])
            self._db.execute(f'''
                UPDATE {self.TABLE_NAME}
                SET {set_statement}
                WHERE {self.primary_key_column().db_column} = ?
                ''', values)

    def refresh_from_db(self):
        column_statement = ', '.join([col.name for col in self.mapped_columns()])
        select_query = f'''
            SELECT {column_statement} FROM {self.TABLE_NAME}
            WHERE {self.primary_key_column().db_column} = ?
        '''
        self._db.execute(select_query, (getattr(self, self.primary_key_column().name),))
        row = self._db.fetchone()

        for idx, col in enumerate(self.mapped_columns()):
            obj_or_val = row[idx]
            if col.col_type == ColumnType.FOREIGN_KEY:
                obj_or_val = col.klass.get(obj_or_val)
            setattr(self, col.name, obj_or_val)

    def __repr__(self):
        return str(self)

    @classmethod
    def commit(cls):
        cls._db.commit()

    @classmethod
    def rollback(cls):
        cls._db.rollback()
