import sqlite3
import crypt_handler


# database entry object containing all the information nessecary
class DbEntry():
    def __init__(self, app, url, email, username, password):
        self.app = app
        self.url = url
        self.email = email
        self.username = username
        self.password = password

    def __str__(self):
        return f'Application: {self.app} | Url: {self.url} | Email: {self.email} | Username: {self.username} | Password: {self.password}'

# create a connection to the database
def create_connection(db):
    con = None

    try:
        con = sqlite3.connect(f'{db}.db')
    except Exception as e:
        print(e)

    return con


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
                Password text,
                primary key (Application, Email)
            )'''
        )

# insert master password to the master table
def insert_to_master(con, password):
    hashed = crypt_handler.hash_password(password)

    with con:
        c = con.cursor()
        c.execute('INSERT INTO master VALUES (:password)', {"password": hashed})

# insert account to the accounts table
def insert_to_accounts(con, entry):
    with con:
        c = con.cursor()
        c.execute('INSERT INTO accounts VALUES(?, ?, ?, ?, ?)', (entry.app, entry.url, entry.email, entry.username, entry.password))

# check if table is empty
def is_empty(con, table):
    with con:
        c =con.cursor()
        c.execute(f'SELECT count(*) FROM {table}')
        res = c.fetchall()[0][0]
    
    return True if res == 0 else False

# return the master password
def get_master_hashed(con):
    with con:
        c = con.cursor()
        c.execute('SELECT Password FROM master')
        res = c.fetchall()[0][0]
        return res

# find accounts by application name
def find_by_app(con, app):
    with con:
        c = con.cursor()
        c.execute('Select * FROM accounts WHERE Application = :app', {'app': app})
        return c.fetchall()

#find accounts by email
def find_by_email(con, email):
    with con:
        c = con.cursor()
        c.execute('Select * FROM accounts WHERE Email=:email', {'email': email})
        return c.fetchall()

# get all the accounts in the database
def show_all(con):
    with con:
        c = con.cursor()
        c.execute('SELECT * FROM accounts')
        return c.fetchall()

# delete an account from the database
def delete_account(con, entry):
    with con:
        c = con.cursor()
        c.execute('DELETE FROM accounts WHERE (Application = :app AND Email = :email)', {'app': entry.app, 'email': entry.email})

# change a password for a chosen account
def change_password(con, entry, new_pass):
    with con:
        c = con.cursor()
        c.execute('UPDATE accounts SET Password = :password WHERE (Application = :app AND Email = :email)', {'password': new_pass, 'app': entry.app, 'email': entry.email})
