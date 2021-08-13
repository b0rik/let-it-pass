import database

menu_options = 3

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
    
    show_results(result)

def show_results(result):
    # result list is not empty
    if result:
        for acc in result:
            app, url, email, username, password = acc
            print(database.DbEntry(app, url, email, username, password))
    # no results
    else:
        print('No results found.')

options = {1: find_menu, 2: insert_menu}