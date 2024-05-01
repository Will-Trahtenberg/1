from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
import settings as st
from hashlib import sha1


class LoginPassword(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        lay = QVBoxLayout(self)

        lay_login = QVBoxLayout()
        lay_login.setSpacing(0)
        login_tit = QLabel('Логин', parent=self)
        self.__login_edt = QLineEdit(parent=self)
        lay_login.addWidget(login_tit)
        lay_login.addWidget(self.__login_edt)
        lay.addLayout(lay_login)

        lay_pwd = QVBoxLayout()
        lay_pwd.setSpacing(0)
        password_tit = QLabel('Пароль', parent=self)
        self.__password_edt = QLineEdit(parent=self)
        self.__password_edt.setEchoMode(QLineEdit.Password)
        lay_pwd.addWidget(password_tit)
        lay_pwd.addWidget(self.__password_edt)
        lay.addLayout(lay_pwd)

        lay_btn = QHBoxLayout()
        lay_btn.addStretch()
        ok = QPushButton('OK', parent=self)
        cancel = QPushButton('Отмена', parent=self)
        lay_btn.addWidget(ok)
        lay_btn.addWidget(cancel)
        lay.addLayout(lay_btn)

        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

    @property
    def login(self):
        return self.__login_edt.text().strip()

    @property
    def password(self):
        result = self.__password_edt.text().strip()
        if result == '':
            return None
        return result


class ChangePassword(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        lay = QVBoxLayout(self)

        lay_pwd = QVBoxLayout()
        lay_pwd.setSpacing(0)
        password_tit = QLabel('Пароль', parent=self)
        self.__password_edt = QLineEdit(parent=self)
        self.__password_edt.setEchoMode(QLineEdit.Password)
        lay_pwd.addWidget(password_tit)
        lay_pwd.addWidget(self.__password_edt)
        lay.addLayout(lay_pwd)

        lay_rpt = QVBoxLayout()
        lay_rpt.setSpacing(0)
        repeat_tit = QLabel('Пароль еще раз', parent=self)
        self.__repeat_edt = QLineEdit(parent=self)
        self.__repeat_edt.setEchoMode(QLineEdit.Password)
        lay_rpt.addWidget(repeat_tit)
        lay_rpt.addWidget(self.__repeat_edt)
        lay.addLayout(lay_rpt)

        lay_btn = QHBoxLayout()
        lay_btn.addStretch()
        ok = QPushButton('OK', parent=self)
        lay_btn.addWidget(ok)
        lay.addLayout(lay_btn)

        ok.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        rpt = self.__repeat_edt.text().strip()
        pwd = self.password
        if rpt == pwd and pwd != '':
            self.accept()

    @property
    def password(self):
        result = self.__password_edt.text().strip()
        if result == '':
            return None
        return result


def check_password(password, pwd_hash, salt):
    return password_hash(password, salt) == pwd_hash


def password_hash(password, salt):
    check = st.global_salt + password + salt
    check = check.encode('utf-8')
    return sha1(check).hexdigest()
