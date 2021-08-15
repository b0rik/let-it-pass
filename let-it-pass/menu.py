import database
import crypt_handler

# number of options in the main menu
MENU_OPTIONS = 4

# initial login menu using the master password
def login(con):
    # check if there is a master password already set
    if database.is_empty(con, 'master'):
        # set master password
        while True:
            print('-' * 20)
            password = input('Enter a master password:\n ')
            print('-' * 20)
            verify = input('Enter again to verify:\n')
            print('-' * 20)

            if password == verify:
                # set master password in database
                database.insert_to_master(con, password)
                print('-' * 20)
                print('Master password has been set.')
                print('-' * 20)
                break
            else:
                print('-' * 20)
                print('Password did not match')
                print('-' * 20)

    # login with master password
    while True:
        print('-' * 20)
        password = input('Enter the master password: \n')
        print('-' * 20)

        # get hashed password from database
        hashed = database.get_master_hashed(con)

        # validate enter password
        if crypt_handler.check_password(password, hashed):
            break
        else:
            print('-' * 20)
            print('The password is incorrect')
            print('-' * 20)

    # create and return a key for encryption based on master password
    key = crypt_handler.make_key(password)
    return key

# show the initial menu
def start_menu():
    while True:
        print('-' * 20)
        print('1.Find account.')
        print('2.Add account.')
        print('3.Show all the accounts.')
        print('0.Quit.')
        selection = int(input('What would you like to do?\n'))
        print('-' * 20)

        if 0 <= selection < MENU_OPTIONS:
            return selection
        else:
            print('-' * 20)
            print('Invalid selection.\n')
            print('-' * 20)

# the menu for addeing account to the database
def insert_menu(con, key):
    # get the user input
    print('-' * 20)
    app = input('Enter the application name:\n')
    print('-' * 20)
    url = input('Enter the url for the app site:\n')
    print('-' * 20)
    email = input('Enter the account email:\n')
    print('-' * 20)
    username = input('Enter the account username:\n')
    print('-' * 20)
    password = input('Enter the account password:\n')
    print('-' * 20)

    #encrpt the password
    encrypted_password = crypt_handler.encrypt_password(password, key)

    entry = database.DbEntry(app, url, email, username, encrypted_password)

    # insert account to the database
    database.insert_to_accounts(con, entry)
    print('-' * 20)
    print('Account has been added.')
    print('-' * 20)

# menu for searching in the database
def find_menu(con, key):
    while True:
        # get user selected finding option
        print('-' * 20)
        selection = input('Would you like to find an account by application name(a) or email(e)?\n')
        print('-' * 20)

        if selection in ('a', 'e'):
            break
        else:
            print('-' * 20)
            print('Invalid option.')
            print('-' * 20)

    # find account based on user selected option
    if selection == 'a':
        print('-' * 20)
        app = input("Enter the name of the application:\n")
        print('-' * 20)
        result = database.find_by_app(con, app)
    else:
        print('-' * 20)
        email = input('Enter the email:\n')
        print('-' * 20)
        result = database.find_by_email(con, email)
    
    show_results(con, result, key)

# decrypt passwords of found results in the database and show the results in a nice way
def show_results(con, result, key):
    # result list is not empty
    if result:
        print('-' * 20)
        for acc in result:
            app, url, email, username, password = acc
            # decrypt the passwords
            decrypted_password = crypt_handler.decrypt_password(password, key)
            res_ind = result.index(acc)
            print(f'{res_ind}.' + str(database.DbEntry(app, url, email, username, decrypted_password.decode('utf8'))))
        print('-' * 20)

        #s show options to delete and account or change a password
        change_delete_menu(con, result, key)
    # no results
    else:
        print('-' * 20)
        print('No results found.')
        print('-' * 20)

# menu for chaning a password or deleting an account
def change_delete_menu(con, result, key):
    while True:
        print('-' * 20)
        selection = input('Would you like to delete(d) an account, change a password(c) or return to main menu(q)?\n')
        print('-' * 20)

        if selection in ('d', 'c', 'q'):
            break
        else:
            print('-' * 20)
            print('Invalid selection.')
            print('-' * 20)
    
    # delete an account
    if selection == 'd':
        while True:
            print('-' * 20)
            acc_to_delete = int(input('Enter the number of the account you want to delete:\n'))
            print('-' * 20)

            if 0 <= acc_to_delete < len(result):
                break
            else:
                print('-' * 20)
                print('Invalid option.')
                print('-' * 20)
        
        # get account credentials and delete it from the database
        app, url, email, username, password = result[acc_to_delete]
        entry = database.DbEntry(app, url, email, username, password)
        database.delete_account(con, entry)

        print('-' * 20)
        print('Account deleted.')
        print('-' * 20)

    # change a password
    elif selection == 'c':
        while True:
            print('-' * 20)
            acc_to_update = int(input('Enter the number of the account you want to update:\n'))
            print('-' * 20)

            if 0 <= acc_to_update < len(result):
                break
            else:
                print('-' * 20)
                print('Invalid option')
                print('-' * 20)

        # get account credentials
        app, url, email, username, password = result[acc_to_update]
        entry = database.DbEntry(app, url, email, username, password)

        # get new password and encrypt it and change it in the database
        print('-' * 20)
        new_password = input('Enter new password:\n')
        print('-' * 20)
        encrypted_password = crypt_handler.encrypt_password(new_password, key)

        database.change_password(con, entry, encrypted_password)
        print('-' * 20)
        print('Password changed.')
        print('-' * 20)

# a menu for showing all the accounts in the database
def show_all_menu(con, key):
    result = database.show_all(con)
    show_results(con, result, key)

# option execution dictionary
options = {1: find_menu, 2: insert_menu, 3: show_all_menu}