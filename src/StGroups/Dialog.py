from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot


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
