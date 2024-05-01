import sys
import PyQt5.QtWidgets
from PyQt5.QtSql import QSqlDatabase
import psycopg2
from PyQt5.QtSql import QSqlDatabase
import settings as st


class Application(PyQt5.QtWidgets.QApplication):

    def __init__(self, argv):
        super().__init__(argv)


        connection = psycopg2.connect(**st.db_params)
        cursor = connection.cursor()
        if connection:
            print('Connected to database', file=sys.stderr)
        else:
            print('Connection FAILED', file=sys.stderr)


