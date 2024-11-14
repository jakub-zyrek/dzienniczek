import sqlite3

connect = sqlite3.connect('database.db')
cursor = connect.cursor()

zapytanie = "CREATE TABLE grades (id INTEGER PRIMARY KEY AUTOINCREMENT, grade FLOAT, name TEXT, student INTEGER, teacher INTEGER)"

cursor.execute(zapytanie)
connect.commit()