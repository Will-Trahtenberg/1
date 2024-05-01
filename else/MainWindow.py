from PyQt5.QtWidgets import QMainWindow, QMessageBox
from MainMenu import MainMenu
from PyQt5.QtCore import pyqtSlot

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)

        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)

    @pyqtSlot()
    def about(self):
        title = 'Управление контроля учета студентов'
        text = 'Программа для контроля учет студентов'
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление учета студентов')


