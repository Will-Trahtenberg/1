from PyQt5.QtWidgets import QTableView, QMessageBox, QDialog
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
import psycopg2
import settings as st

from .Model import Model
from .Dialog import Dialog


SELECT_ONE = '''
    select f_title, f_comment
        from stgroup
        where id = %s ;
'''


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)

        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)

        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)

        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(2, hh.Stretch)

    @pyqtSlot()
    def add(self):
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.title, dia.comment)

    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        row = self.currentIndex().row()
        id_stgroup = self.model().record(row).value(0)
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_stgroup,)
        cursor.execute(SELECT_ONE, data)
        dia.title, dia.comment = cursor.fetchone()
        conn.close()
        if dia.exec():
            self.model().update(id_stgroup, dia.title, dia.comment)

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_stgroup = self.model().record(row).value(0)
        ans = QMessageBox.question(self, 'Группа', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().delete(id_stgroup)


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Группа')

        title_lbl = QLabel('Наименование', parent=self)
        self.__title_edt = QLineEdit(parent=self)

        comment_lbl = QLabel('Примечание', parent=self)
        self.__comment_edt = QTextEdit(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)

        lay_tit = QVBoxLayout()
        lay_tit.setSpacing(0)
        lay_tit.addWidget(title_lbl)
        lay_tit.addWidget(self.__title_edt)
        lay.addLayout(lay_tit)

        lay_con = QVBoxLayout()
        lay_con.setSpacing(0)
        lay_con.addWidget(comment_lbl)
        lay_con.addWidget(self.__comment_edt)
        lay.addLayout(lay_con)

        lay2 = QHBoxLayout()
        lay2.addStretch()
        lay2.addWidget(ok_btn)
        lay2.addWidget(cancel_btn)
        lay.addLayout(lay2)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        if self.title is None:
            return
        self.accept()

    @property
    def title(self):
        result = self.__title_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @title.setter
    def title(self, value):
        self.__title_edt.setText(value)

    @property
    def comment(self):
        result = self.__comment_edt.toPlainText().strip()
        if result == '':
            return None
        else:
            return result

    @comment.setter
    def comment(self, value):
        self.__comment_edt.setPlainText(value)
