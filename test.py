import sqlite3

connection = sqlite3.connect('marianos.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text)"
cursor.execute(create_table)

users = [
    (1, 'admin', 'admin'),
    (2, 'user', 'user')
]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
