import database
import menu


# create connection to the database
con = database.create_connection('pass')

if con is None:
    quit()

# create tables
database.create_master_table(con)
database.create_accounts_table(con)

# on first run get a master password
# login using the master password
key = menu.login(con)

# show start menu and get option
while True:
    selection = menu.start_menu()
    if selection != 0:
        menu.options[selection](con, key)
    else:
        break
