import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem
import psycopg2

class DatabaseManager:
    def __init__(self):
        # Установим соединение с базой данных
        self.connection = psycopg2.connect(
            host="localhost",
            database="учет студентов",
            user="postgres",
            password="12345678"
        )
        self.cursor = self.connection.cursor()

    def refresh_table(self, table_widget):
        # Получение данных из базы данных и обновление таблицы
        query = "SELECT * FROM студент"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # Очистим таблицу перед обновлением
        table_widget.clear()
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                table_widget.setItem(i, j, QTableWidgetItem(str(value)))

    def add_record(self):
        # Открытие окна для добавления новой записи
        self.add_edit_window = AddEditRecordWindow(self)
        self.add_edit_window.show()

    def edit_record(self):
        # Открытие окна для редактирования выбранной записи
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            record_id = self.table_widget.item(selected_row, 0).text()
            self.add_edit_window = AddEditRecordWindow(self, record_id)
            self.add_edit_window.show()

    def delete_record(self):
        # Удаление выбранной записи из базы данных
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            record_id = self.table_widget.item(selected_row, 0).text()
            query = f"DELETE FROM студент WHERE код_студента={record_id}"
            self.cursor.execute(query)
            self.connection.commit()
            self.refresh_table()

    def save_record(self, data):
        # Сохранение/обновление записи в базе данных
        if data.get('id'):  # Если есть id, это редактирование
            query = f"UPDATE студент SET код_студента"
        else:  # В противном случае, это добавление новой записи
            query = f"INSERT INTO студент (select код_студента, фио, дата_рождения, номер_зачетной_книжки, статус, номер_телефона, пол from студент) VALUES (code_stud, fio_stud, birth_stud, numb_zachet_stud, status, phone_number, pol)"
        self.cursor.execute(query, data.values())
        self.connection.commit()
        self.refresh_table()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление данными")
        self.setGeometry(100, 100, 600, 400)

        self.db_manager = DatabaseManager()
        self.table_widget = QTableWidget()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.layout.addWidget(self.table_widget)

        self.refresh_table()

        self.add_button = QPushButton("Добавить запись")
        self.add_button.clicked.connect(self.db_manager.add_record)
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Редактировать запись")
        self.edit_button.clicked.connect(self.db_manager.edit_record)
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить запись")
        self.delete_button.clicked.connect(self.db_manager.delete_record)
        self.layout.addWidget(self.delete_button)

    def refresh_table(self):
        self.db_manager.refresh_table(self.table_widget)


class AddEditRecordWindow(QWidget):
    def __init__(self, db_manager, record_id=None):
        super().__init__()
        self.setWindowTitle("Добавить/Редактировать запись")
        self.setGeometry(200, 200, 400, 200)
        self.db_manager = db_manager
        self.record_id = record_id

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.fields = {
            "code": QLineEdit(),
            "name": QLineEdit(),
            # Добавьте остальные поля в соответствии с вашими таблицами
        }

        for field_name, field_widget in self.fields.items():
            field_layout = QHBoxLayout()
            field_layout.addWidget(QLabel(field_name.capitalize()))
            field_layout.addWidget(field_widget)
            self.layout.addLayout(field_layout)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_record)
        self.layout.addWidget(self.save_button)

        if record_id is not None:
            # Если передан идентификатор записи, это редактирование
            self.load_record(record_id)

    def load_record(self, record_id):
        # Загрузка данных выбранной записи для редактирования
        # Здесь нужно выполнить запрос к базе данных и заполнить поля формы
        pass

    def save_record(self):
        # Сохранение/обновление записи в базе данных
        data = {}
        for field_name, field_widget in self.fields.items():
            data[field_name] = field_widget.text()
        if self.record_id is not None:
            data['id'] = self.record_id
        self.db_manager.save_record(data)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
