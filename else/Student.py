import sys

import psycopg2
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtSql import QSqlDatabase
import settings as st
from PyQt5.QtWidgets import QTableView, QMessageBox, QDialog, QLabel, QLineEdit, QPushButton, QTableWidgetItem

insert = '''insert into студент(код_студента, фио, дата_рождения, 
    номер_зачетной_книжки, статус, номер_телефона, пол, id_user) values (%s, %s,%s,%s,%s,%s,%s,%s);'''

SELECT_ALL = '''select код_студента, фио, дата_рождения, номер_зачетной_книжки, статус, номер_телефона, пол from студент'''

UPDATE = '''
    update студент set
           фио = %s,
           дата_рождения = %s,
           номер_зачетной_книжки = %s,
           статус = %s,
           номер_телефона = %s,
           пол = %s,
           id_user = %s
        where код_студента = %s ;
'''

class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)



        def obnovit(self):
            self.setQuery(SELECT_ALL)

        def add(self, code_stud, fio_stud, birth_stud, numb_zachet_stud, status, phone_number, pol):
            conn = psycopg2.connect(**st.db_params)
            cursor = conn.cursor()

            data = (code_stud, fio_stud, birth_stud, numb_zachet_stud, status, phone_number, pol)
            cursor.execute(SELECT_ALL, data)
            conn.commit()
            conn.close()
            self.obnovit()


        def update(self, code_stud, fio_stud, birth_stud, numb_zachet_stud, status, phone_number, pol):
            conn = psycopg2.connect(**st.db_params)
            cursor = conn.cursor()
            data = (code_stud, fio_stud, birth_stud, numb_zachet_stud, status, phone_number, pol)
            cursor.execute(UPDATE, data)



class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)


    @pyqtSlot()
    def add(self):
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.code_stud, dia.fio_stud, dia.birth_stud, dia.numb_zachet_stud, dia.status, dia.phone_number, dia.pol)

    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        row = self.currentIndex().row()
        code_stud = self.model().record(row).value(0)
        fio_stud = self.model().record(row).value(1)
        birth_stud = self.model().record(row).value(2)
        numb_zachet_stud = self.model().record(row).value(3)
        status = self.model().record(row).value(4)
        phone_number = self.model().record(row).value(5)
        pol = self.model().record(row).value(6)
        data = (code_stud, fio_stud, birth_stud, numb_zachet_stud, status, phone_number, pol)
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute( UPDATE, data)
        if dia.exec():
            self.model().update(code_stud, dia.fio_stud, dia.birth_stud, dia.numb_zachet_stud, dia.status, dia.phone_number, dia.pol)

        QMessageBox.information(self, 'студент', 'редактировать')

    def delete(self):
        QMessageBox.information(self, 'студент', 'удалить')

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        fio_studenta_lbl = QLabel('Фамилия И.О.', parent=self)
        self.__fio_studenta = QLineEdit(parent=self)

        phone_lbl = QLabel('Телефон', parent=self)
        self.__phone_lbl = QLineEdit(parent=self)

        ok_btn = QPushButton('Ok', parent=self)
        cancel_btn = QPushButton('Cancel', parent=self)


