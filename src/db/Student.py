from dataclasses import dataclass
import psycopg2
from src import settings as st


INSERT_USER = '''
    insert into appuser( f_login, f_salt, f_role )
       values( %s, %s, 'student' )
       returning id ;
'''

INSERT_STUDENT = '''
    insert into student ( f_fio, f_email, f_comment, id_user )
       values( %s, %s, %s, %s )
       returning id ;
'''

UPDATE_STUDENT = '''
    update student set
            f_fio = %s,
            f_email = %s,
            f_comment = %s
        where id = %s ;
'''


SELECT_ONE = '''
    select
          u.f_login,
          s.f_fio,
          s.f_email,
          s.f_comment,
          s.id_user
       from appuser as u
       inner join student as s
          on u.id = s.id_user
       where s.id = %s ;
'''


@dataclass
class Student(object):

    pk: int = None
    login: str = None
    fio: str = None
    email: str = None
    comment: str = None
    id_user: int = None

    @property
    def user_data(self):
        return (self.login, '1')

    @property
    def student_data(self):
        return (self.fio, self.email, self.comment, self.id_user)

    @property
    def student_upd_data(self):
        return (self.fio, self.email, self.comment, self.pk)

    def insert(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(INSERT_USER, self.user_data)
        (self.id_user,) = next(cursor)
        cursor.execute(INSERT_STUDENT, self.student_data)
        (self.pk,) = next(cursor)
        conn.commit()
        conn.close()

    def update(self):
        conn = psycopg2.connect(**st.db_params)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(UPDATE_STUDENT, self.student_upd_data)
        finally:
            conn.close()

    def save(self):
        if self.pk is None:
            return self.insert()
        else:
            return self.update()

    def load(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(SELECT_ONE, (self.pk,))
        (self.login, self.fio,
         self.email, self.comment, self.id_user) = next(cursor)
        conn.commit()
        conn.close()
        return self

