import sqlite3
import hashlib
import db_opr

def hash_password(pw):
    h = hashlib.sha256()
    h.update(pw.encode())
    return h.hexdigest()

def add_new_stored_password(conn):
    platform = input('Please enter the name of the platform: ')
    username = input('Please enter the username you use in the platform: ')
    email = input('Please enter the email you use in the platform: ')
    password = input('Please enter the email you use in the platform: ')



def update_password(conn):
    while True:
        row_id = input('\nPlease enter the id of the row you want to update')
        if db_opr.check_row_id(conn, row_id):
            break
        else:
            print('The row id you typed could not be found in db')
            print('Please try again!\n')

    platform = input('Please enter name of the platform: ')
    username = input('Please enter username for the account: ')
    email = input('Please enter email for the account: ')
    password = input('Please enter the new password for the account: ')

    if db_opr.update_account_values(conn, row_id, platform, username, email, password):
        print('Congrats! Successfully updated!')
    else:
        print('Something went wrong!')

def delete_password(conn):
    while True:
        row_id = input('\nPlease enter the id of the row you want to DELETE')
        if db_opr.check_row_id(conn, row_id):
            break
        else:
            print('The row id you typed could not be found in db')
            print('Please try again!\n')
    
    row = db_opr.get_account_row(conn, row_id)
    if row:
        print('Are you sure to delete this below ?')
        print(row)
        last_call = input('y/n: ')
        if last_call == 'y':
            if db_opr.delete_stored_password(conn, row_id):
                print('Successfully deleted!')
            else:
                print('Something went wrong!')
        elif last_call == 'n':
            print('Delete operation is cancelled')
        else:
            print('Invalid option')
    else:
        print('Something went wrong!')

def delete_program_user_acc(conn, user_id):
    while True:
        pw = input('Please enter your program password in order to confirm deletion: ')
        hashed_pw = hash_password(pw)

        user = db_opr.get_program_user(conn, user_id)

        if hashed_pw == user[2]:
            print('Delete operation is confirmed!')
            if db_opr.delete_program_user(conn, user_id):
                print('Deletion is successful!')
                break
            else:
                print('Incorrect password! Try again.')
        else:
            print('Incorrect password! Try again.')
    welcome_page(conn)
    
def recognized_user(conn, user_id):
    print('Hello user')
    stored_passwords = db_opr.get_stored_passwords(conn, user_id)
    if stored_passwords:
        print('Here is the list of your stored passwords')
    else:
        print('No stored password found in your account!')

    while True:
        print('What do you desire to do?')
        print('(1) Log out')
        print('(2) Add a new password')
        print('(3) Update a stored password')
        print('(4) Delete a stored password')
        print('(5) Delete my whole account')
        option = input('Option: ')

        if option == '1':
            break
        elif option == '2':
            add_new_stored_password(conn)
        elif option == '3':
            update_password(conn)
        elif option == '4':
            delete_password(conn)
        elif option == '5':
            delete_program_user_acc(conn, user_id)
        else:
            print('Invalid option! Please try again')

    print('Bye!')


def login(conn):
    while True:
        username = input('\nPlease enter your username: ')
        password = input('Please enter your password: ')

        hashed_pw = hash_password(password)
        user_id_tuple = db_opr.check_user(conn, username, hashed_pw)

        if user_id_tuple:
            break

        print('Username or password might be incorrect')
        print('Please try again\n')
    
    recognized_user(conn, user_id_tuple[0])


def new_user(conn):
    while True:
        username = input('\nPlease enter a username: ')
        password = input('Please enter a password: ')

        hashed_pw = hash_password(password)
        user_id = db_opr.add_user(conn, username, hashed_pw)

        if user_id:
            break

    print('New user {} successfully added'.format(username))
    recognized_user(conn, user_id)


def welcome_page(conn):
    print('Welcome to PasswordManagerNoUI')
    print('What do you desire?')
    while True:
        print('Press 1 for login')
        print('Press 2 for register')
        option = input('\nOption: ')
        if option not in ('1', '2'):
            print('Invalid input, please try again')
        else:
            break

    if option == '1':
        login(conn)
    elif option == '2':
        new_user(conn)

if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    welcome_page(conn)
    conn.close()
