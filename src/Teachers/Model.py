from PyQt5.QtSql import QSqlQueryModel
import psycopg2
import settings as st


SELECT_ALL = '''
    select id, f_fio, f_phone, f_email, f_comment
        from teacher ;
'''


SELECT_ONE = '''
    select f_fio, f_phone, f_email, f_comment
        from teacher
        where id = %s ;
'''


UPDATE = '''
    update teacher set
           f_fio = %s,
           f_phone = %s,
           f_email = %s,
           f_comment = %s
        where id = %s ;
'''


DELETE = '''
    delete from teacher where id = %s ;
'''


class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.obnovit()

    def obnovit(self):
        self.setQuery(SELECT_ALL)

    def update(self, id_teacher, fio, phone, email, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (fio, phone, email, comment, id_teacher)
        cursor.execute(UPDATE, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def delete(self, id_teacher):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_teacher,)
        cursor.execute(DELETE, data)
        conn.commit()
        conn.close()
        self.obnovit()
