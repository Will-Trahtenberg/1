from PyQt5.QtWidgets import QTableView, QMessageBox
from PyQt5.QtCore import pyqtSlot
import db

from .Model import Model
from .Dialog import Dialog


SELECT_ONE = '''
    select f_fio, f_phone, f_email, f_comment
        from teacher
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
        hh.setSectionResizeMode(4, hh.Stretch)

    @property
    def pk(self):
        row = self.currentIndex().row()
        return self.model().record(row).value(0)

    @pyqtSlot()
    def add(self):
        dia = Dialog(parent=self)
        if dia.exec():
            data = db.Teacher()
            dia.get(data)
            data.save()
            self.model().obnovit()

    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        data = db.Teacher(pk=self.pk).load()
        dia.put(data, for_update=True)
        if dia.exec():
            dia.get(data)
            data.save()
            self.model().obnovit()

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        ans = QMessageBox.question(self, 'Учитель', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().delete(id_teacher)
