import sqlite3

def create_table():
    with sqlite3.connect('pass.db') as con:
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
            Application text,
            Username text,
            Email text,
            Password text
        )''')

        con.commit()

def insert_to_table(app, user, email, password):
    with sqlite3.connect('pass.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO accounts VALUES (?, ?, ?, ?)', (app, user, email, password))
        con.commit()

def show_all():
    with sqlite3.connect('pass.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM accounts')
        print(cur.fetchall())

def delete_all():
    with sqlite3.connect('pass.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM accounts')
        con.commit()

# TODO:
# 1.create table
# 2.get master password
# 3.show menu
# ...

create_table()
