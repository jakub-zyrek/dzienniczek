import sqlite3

connect = sqlite3.connect('database.db')
cursor = connect.cursor()

zapytanie = "INSERT INTO students_class (student_id, class_id) VALUES (3, 3), (3, 3)"
zapytanie1 = "DELETE FROM students_class WHERE student_id = 3"

cursor.execute(zapytanie)
connect.commit()