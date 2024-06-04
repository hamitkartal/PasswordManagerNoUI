from sqlite3 import Error

############ OPERATIONS FOR THE TABLE "USERS" ############
#####################################################################

# checks if username&password pair
# exists in the db, in the logging phase
# returns id, if exists
# returns None, otherwise

def check_user(conn, un, h_pw):
    try:
        query = 'SELECT id FROM users WHERE username = ? AND password = ? LIMIT 1'
        cu = conn.cursor()
        cu.execute(query, (un, h_pw))
        return cu.fetchone()
    except Error as e:
        print('An error occured {e}'.format(e))
        return None

# adds a new user (username & password pair)
# into the database, in the registeration phase
def add_user(conn, un, h_pw):
    try:
        cu = conn.cursor()
        query = 'INSERT INTO users (username, password) VALUES (?, ?)'
        cu.execute(query, (un, h_pw))
        conn.commit()
        return cu.lastrowid
    except Error as e:
        print('An error occured {e}'.format(e))
        return None

# returns the complete row based on the user id
def get_program_user(conn, user_id):
    try:
        cu = conn.cursor()
        query = 'SELECT * FROM users WHERE id = ?'
        cu.execute(query, (user_id,))
        return cu.fetchone()
    except Error as e:
        print('An error occured {}'.format(e))
        return None

# deletes the program user
# utilizes <delete_stored_password_by_user_id>
# function. purpose is not leaving any stored_password
# for a deleted user
def delete_program_user(conn, user_id):
    if not delete_stored_password_by_user_id(conn, user_id):
        print('Stored passwords of the user could not be deleted from stored_passwords table')
        return False
    else:
        try:
            cu = conn.cursor()
            query = 'DELETE FROM users WHERE id = ?'
            cu.execute(query, (user_id,))
            conn.commit()
        except Error as e:
            print('An error occured {}'.format(e))
            print('Stored passwords of the user are deleted successfully')
            print('But, the user itself could not be deleted from the users table')
            return False
        return True

# TODO
# this feature will be added later
# user will be able to delete his
# account from the program
def delete_user():
    pass

# TODO
# this feature will be added later
# user will be able to update his
# user password
def update_user_pw():
    pass

############ OPERATIONS FOR THE TABLE "STORED_PASSWORDS" ############
#####################################################################

def add_stored_password(conn, user_id, platform, un, email, pw):
    try:
        cu = conn.cursor()
        query = 'INSERT INTO stored_passwords (user_id, platform_name, username, email, password, last_update) \
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)'
        cu.execute(query, (user_id, platform, un, email, pw))
        conn.commit()
    except Error as e:
        print('An error occured: {}'.format(e))
        return False
    return True

# gets all the stored_password for given user id
def get_stored_passwords(conn, user_id):
    cu = conn.cursor()
    query = 'SELECT * FROM stored_passwords WHERE user_id = ?'
    cu.execute(query, (user_id, ))
    return cu.fetchall()

# checks if a given id exists in the "stored_passwords" table
def check_row_id(conn, row_id):
    try:
        cu = conn.cursor()
        query = 'SELECT 1 FROM stored_passwords WHERE id = ? LIMIT 1'
        cu.execute(query, (row_id, ))
        return cu.fetchone() is not None
    except Error as e:
        print('An error occured {e}'.format(e))
        return None

# updates values for a given stored_password_id (row_id)
def update_account_values(conn, row_id, platform, username, email, password):
    try:
        cu = conn.cursor()
        query = '''
        UPDATE stored_passwords
        SET platform_name = ?, username = ?, email = ?, password = ?, last_update = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        cu.execute(query, (row_id, platform, username, email, password))
        conn.commit()
    except Error as e:
        print('An error occured: {}'.format(e))
        return False
    return True

# get a single row (account) by given a row_id (stored_password id)
def get_account_row(conn, row_id):
    try:
        cu = conn.cursor()
        query = '''
        SELECT *
        FROM stored_passwords
        WHERE id = ?
        '''
        cu.execute(query, (row_id,))
        return cu.fetchall()
    except Error as e:
        print('An error occured: {}'.format(e))
        return None

# deletes a single row (account) by given a row_id (stored_password id)
def delete_stored_password(conn, row_id):
    try:
        cu = conn.cursor()
        query = '''
        DELETE FROM stored_passwords
        WHERE id = ?
        '''
        cu.execute(query, (row_id,))
        conn.commit()
    except Error as e:
        print('An error occured: {}'.format(e))
        return False
    return True

# deletes all the rows (account) by given user_id
def delete_stored_password_by_user_id(conn, user_id):
    try:
        cu = conn.cursor()
        query = 'DELETE FROM stored_passwords WHERE user_id = ?'
        cu.execute(query, (user_id,))
        conn.commit()
    except Error as e:
        print('An error occured {}'.format(e))
        return False
    return True
