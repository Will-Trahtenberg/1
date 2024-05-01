from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from .Ui_StudentFrame import Ui_StudentFrame


class _Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_StudentFrame()
        self.ui.setupUi(self)


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Студент')

        self.__frame = _Frame(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)

        lay.addWidget(self.__frame)

        lay2 = QHBoxLayout()
        lay2.addStretch()
        lay2.addWidget(ok_btn)
        lay2.addWidget(cancel_btn)
        lay.addLayout(lay2)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        if self.fio is None:
            return
        self.accept()

    @property
    def login(self):
        result = self.__frame.ui.login_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @login.setter
    def login(self, value):
        self.__frame.ui.login_edt.setText(value)

    @property
    def fio(self):
        result = self.__frame.ui.fio_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @fio.setter
    def fio(self, value):
        self.__frame.ui.fio_edt.setText(value)

    @property
    def phone(self):
        result = self.__frame.ui.phone_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @phone.setter
    def phone(self, value):
        self.__frame.ui.phone_edt.setText(value)

    @property
    def email(self):
        result = self.__frame.ui.email_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @email.setter
    def email(self, value):
        self.__frame.ui.email_edt.setText(value)

    @property
    def comment(self):
        result = self.__frame.ui.comment_edt.toPlainText().strip()
        if result == '':
            return None
        else:
            return result

    @comment.setter
    def comment(self, value):
        self.__frame.ui.comment_edt.setPlainText(value)

    def get(self, data):
        data.login = self.login
        data.fio = self.fio
        data.email = self.email
        data.comment = self.comment

    def put(self, data, *, for_update=False):
        self.login = data.login
        self.fio = data.fio
        self.email = data.email
        self.comment = data.comment
        self.__frame.ui.login_edt.setReadOnly(for_update)

