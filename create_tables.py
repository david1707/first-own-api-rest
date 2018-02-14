import sqlite3

connection = sqlite3.connect('marianos.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS dishes (id INTEGER PRIMARY KEY, name text, price real, type text)"
cursor.execute(create_table)

connection.commit()
connection.close()
