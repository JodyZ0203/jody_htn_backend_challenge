import sqlite3

connection = sqlite3.connect('htn.db')


with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (user_id, name, email, company, phone) VALUES  ('sdfhksfa','James','james@pynative.com','htn','6472023422')")

connection.commit()
connection.close()