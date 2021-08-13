import sqlite3

class DbEntry():
    def __init__(self, app, url, email, username, password):
        self.app = app
        self.url = url
        self.email = email
        self.username = username
        self.password = password

# create a connection to the database
def create_connection(db):
    return sqlite3.connect(f'{db}.db')

# create a table for the master password
def create_master_table(con):
    with con:
        c = con.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS master (Password text)')

# create a table for the accounts
def create_accounts_table(con):
    with con:
        c = con.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                Application text,
                Url text,
                Email text,
                Username text,
                Password text
            )'''
        )

# insert master password to the master table
def insert_to_master(con, password):
    with con:
        c = con.cursor()
        c.execute('INSERT INTO master VALUES (:password)', {"password": password})

# insert account to the accounts table
def insert_to_accounts(con, entry):
    with con:
        c = con.cursor()
        c.execute('INSERT INTO accounts VALUES(?, ?, ?, ?, ?)', (entry.app, entry.url, entry.email, entry.username, entry.password))

#delete from accounts table
def delete_account(con, entry):
    pass

# check if table is empty
def is_empty(con, table):
    with con:
        c =con.cursor()
        c.execute(f'SELECT count(*) FROM {table}')
        res = c.fetchall()[0][0]
    
    return True if res == 0 else False

# return the master password
def get_master_password(con):
    with con:
        c = con.cursor()
        c.execute('SELECT Password FROM master')
        res = c.fetchall()[0][0]
        return res

# find accounts by application name
def find_by_app(con, app):
    c = con.cursor()

    c.execute('Select * FROM accounts WHERE Application=:app', {'app': app})
    return c.fetchall()

#find accounts by email
def find_by_email(con, email):
    c = con.cursor()

    c.execute('Select * FROM accounts WHERE Email=:email', {'email': email})
    return c.fetchall()
