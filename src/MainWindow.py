from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSlot
from MainMenu import MainMenu
import Teachers
import Students
import StGroups
from Login import LoginPassword, ChangePassword, check_password
from Login import password_hash
import psycopg2
import settings as st
from datetime import datetime


SELECT_LOGIN = '''
    select id, f_login, f_password_hash, f_enabled, f_expire, f_role, f_salt
        from appuser
        where f_login = %s ;
'''

UPDATE_PHASH = '''
    update appuser set
        f_password_hash = %s
        where id = %s ;
'''


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)

        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)
        main_menu.teacher_mode_request.connect(self.teacher_mode_on)
        main_menu.student_mode_request.connect(self.student_mode_on)
        main_menu.stgroup_mode_request.connect(self.stgroup_mode_on)

        if not self.authorize():
            main_menu.lock()

    def authorize(self):
        dia = LoginPassword(self)
        if not dia.exec():
            return False
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (dia.login,)
        cursor.execute(SELECT_LOGIN, data)
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return False
        id_user, login, pwd_hash, enabled, expire, role, salt = data
        if not enabled:
            return False
        if expire is not None:
            if expire < datetime.now():
                return False
        if pwd_hash is None:
            if dia.password is not None:
                return False
            dia2 = ChangePassword(parent=self)
            if not dia2.exec():
                return False
            data = (password_hash(dia2.password, salt), id_user,)
            conn = psycopg2.connect(**st.db_params)
            cursor = conn.cursor()
            cursor.execute(UPDATE_PHASH, data)
            conn.commit()
            conn.close()
        else:
            if not check_password(dia.password, pwd_hash, salt):
                return False
        QApplication.instance().set_authorized(login, role)
        return True

    @pyqtSlot()
    def about(self):
        title = 'Управление заданиями для учащихся'
        text = ('Программа для управления задачами\n' +
                'и заданиями для учащихся школы')
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление заданиями для учащихся')

    @pyqtSlot()
    def teacher_mode_on(self):
        old = self.centralWidget()
        v = Teachers.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_teacher(v)
        if old is not None:
            old.deleteLater()

    @pyqtSlot()
    def student_mode_on(self):
        old = self.centralWidget()
        v = Students.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_student(v)
        if old is not None:
            old.deleteLater()

    @pyqtSlot()
    def stgroup_mode_on(self):
        old = self.centralWidget()
        v = StGroups.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_stgroup(v)
        if old is not None:
            old.deleteLater()
