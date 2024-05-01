from PyQt5.QtWidgets import QTableView, QMessageBox
from PyQt5.QtCore import pyqtSlot
import db

from .Model import Model
from .Dialog import Dialog


SELECT_ONE = '''
    select f_fio, f_email, f_comment
        from student
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
        hh.setSectionResizeMode(3, hh.Stretch)

    @property
    def pk(self):
        row = self.currentIndex().row()
        return self.model().record(row).value(0)

    @pyqtSlot()
    def add(self):
        dia = Dialog(parent=self)
        if dia.exec():
            data = db.Student()
            dia.get(data)
            data.save()
            self.model().obnovit()

    @pyqtSlot()
    def update(self):
        # @FIXME При редактировании без выбора студента выдается ошибка
        dia = Dialog(parent=self)
        data = db.Student(pk=self.pk).load()
        dia.put(data)
        if dia.exec():
            dia.get(data)
            data.save()
            self.model().obnovit()

    @pyqtSlot()
    def delete(self):
        # @FIXME при удалении без выбора студента удаляется первый по списку
        row = self.currentIndex().row()
        id_student = self.model().record(row).value(0)
        ans = QMessageBox.question(self, 'Студент', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().delete(id_student)
