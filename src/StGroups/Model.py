from PyQt5.QtSql import QSqlQueryModel
import psycopg2
import settings as st


SELECT_ALL = '''
    select id, f_title, f_comment
        from stgroup ;
'''

INSERT = '''
    insert into stgroup ( f_title, f_comment )
        values ( %s, %s ) ;
'''

SELECT_ONE = '''
    select f_title, f_comment
        from stgroup
        where id = %s ;
'''

UPDATE = '''
    update stgroup set
           f_title = %s,
           f_comment = %s
        where id = %s ;
'''

DELETE = '''
    delete from stgroup where id = %s ;
'''


class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.obnovit()

    def obnovit(self):
        self.setQuery(SELECT_ALL)

    def add(self, title, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (title, comment)
        cursor.execute(INSERT, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def update(self, id_stgroup, title, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (title, comment, id_stgroup)
        cursor.execute(UPDATE, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def delete(self, id_stgroup):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_stgroup,)
        cursor.execute(DELETE, data)
        conn.commit()
        conn.close()
        self.obnovit()
