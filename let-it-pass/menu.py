import database

menu_options = 4

def login(con):
    if database.is_empty(con, 'master'):
        while True:
            print('*' * 20)
            password = input('Enter a master password: ')
            print('*' * 20)
            verify = input('Enter again to verify: ')
            if password == verify:
                database.insert_to_master(con, password)
                print('*' * 20)
                print('Master password has been set.')
                break
            else:
                print('*' * 20)
                print('Password did not match')

    # login with master password
    while True:
        print('*' * 20)
        password = input('Enter the master password: ')
        master = database.get_master_password(con)

        if password == master:
            break
        else:
            print('*' * 20)
            print('The password is incorrect')

# show the initial menu
def start_menu():
    while True:
        print('*' * 20)
        print('1.Find account.')
        print('2.Add account.')
        print('3.Show all the accounts.')
        print('0.Quit.')
        selection = int(input('What would you like to do?\n'))

        if 0 <= selection < menu_options:
            return selection
        else:
            print('*' * 20)
            print('Invalid selection.\n')

def insert_menu(con):
    # get the user input
    print('*' * 20)
    app = input('Enter the application name: ')
    print('*' * 20)
    url = input('Enter the url for the app site: ')
    print('*' * 20)
    email = input('Enter the account email: ')
    print('*' * 20)
    username = input('Enter the account username: ')
    print('*' * 20)
    password = input('Enter the account password: ')

    entry = database.DbEntry(app, url, email, username, password)

    # insert account to the database
    database.insert_to_accounts(con, entry)
    print('*' * 20)
    print('Account has been added.')

def find_menu(con):
    while True:
        # get user selected finding option
        print('*' * 20)
        print('Would you like to find an account by application name(a) or email(e)?')
        selection = input()

        if selection in ('a', 'e'):
            break
        else:
            print('*' * 20)
            print('Invalid option.')

    # find account based on user selected option
    if selection == 'a':
        print('*' * 20)
        app = input("Enter the name of the application :")
        result = database.find_by_app(con, app)
    else:
        print('*' * 20)
        email = input('Enter the email: ')
        result = database.find_by_email(con, email)
    
    show_results(con, result)

def show_results(con, result):
    # result list is not empty
    if result:
        for acc in result:
            app, url, email, username, password = acc
            res_ind = result.index(acc)
            print(f'{res_ind}.' + str(database.DbEntry(app, url, email, username, password)))

        change_delete_menu(con, result)
    # no results
    else:
        print('No results found.')

def change_delete_menu(con, result):
    while True:
        selection = input('Would you like to delete(d) an account, change a password(c) or return to main menu(q)? ')
        if selection in ('d', 'c', 'q'):
            break
        else:
            print('Invalid selection.')
    
    if selection == 'd':
        while True:
            acc_to_delete = int(input('Enter the number of the account you want to delete: '))
            if 0 <= acc_to_delete < len(result):
                break
            else:
                print('Invalid option.')
            
        app, url, email, username, password = result[acc_to_delete]
        entry = database.DbEntry(app, url, email, username, password)
        database.delete_account(con, entry)
        print('Account deleted.')

    elif selection == 'c':
        while True:
            acc_to_update = int(input('Enter the number of the account you want to update: '))
            if 0 <= acc_to_update < len(result):
                break
            else:
                print('Invalid option')

        app, url, email, username, password = result[acc_to_update]
        entry = database.DbEntry(app, url, email, username, password)
        new_pass = input('Enter new password: ')
        database.change_password(con, entry, new_pass)
        print('Password changed.')


        

def show_all_menu(con):
    result = database.show_all(con)
    show_results(con, result)

options = {1: find_menu, 2: insert_menu, 3: show_all_menu}