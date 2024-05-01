import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="учет студентов",
    user="postgres",
    password="12345678"
)

# Создание курсора
cur = conn.cursor()

# Выполнение SQL-запроса
cur.execute("SELECT * FROM студент")

# Получение результатов
rows = cur.fetchall()

# Закрытие соединения с базой данных
cur.close()
conn.close()

# Создание приложения PyQt
app = QApplication(sys.argv)
window = QMainWindow()

# Создание таблицы
table = QTableWidget()
table.setColumnCount(8)
table.setHorizontalHeaderLabels(["Код студента", "ФИО", "Дата рождения", "Номер зачетной книжки", "Статус", "Номер телефона", "Пол", "id_user"])

# Заполнение таблицы данными
table.setRowCount(len(rows))
for row_num, row_data in enumerate(rows):
    for col_num, col_data in enumerate(row_data):
        table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

# Создание виджета для отображения таблицы
widget = QWidget()
layout = QVBoxLayout()
layout.addWidget(table)
widget.setLayout(layout)

# Настройка окна
window.setCentralWidget(widget)
window.setWindowTitle("Студенты")
window.show()

# Запуск приложения
sys.exit(app.exec_())
