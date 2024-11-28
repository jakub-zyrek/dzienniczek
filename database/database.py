import sqlite3

connect = sqlite3.connect('database.db')
cursor = connect.cursor()

zapytanie = "INSERT INTO students_class (student_id, class_id) VALUES (?, ?)"

cursor.execute(zapytanie, [1, 1])
connect.commit()