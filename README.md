# PasswordManagerNoUI
Password Manager without UI

This terminal application is for personal use. It is difficult to memorize every password we have for each platform today. For this need, I built an INSECURE simple python application. Program passwords are kept as hash values in the database. However, the stored passwords of the users are kept plain in the database FOR NOW. In future, they will be kept in decrypted form.<br>Another future feature is, users will be able to change their program passwords.<br>
<br>

------- 2024/06/05
As I researched how to improve the quality of the program and the code, there are several aspects that I can work on:<br>
1) Environment Variables<br>
Instead of hardcoding the .db file, better to use the environment variables for database connection.<br>
<br>

2) Context Managers (For Cursors)<br>
It is important to close the resources after using them. For that reason, context managers could be used. Below is an example: <br>

INSTEAD OF THIS <br>
```
def check_user(conn, un, h_pw):
    try:
        query = 'SELECT id FROM users WHERE username = ? AND password = ? LIMIT 1'
        cu = conn.cursor()
        cu.execute(query, (un, h_pw))
        return cu.fetchone()
    except Error as e:
        print('An error occured {e}'.format(e))
        return None
```

THIS WOULD BE A BETTER PRACTICE
```
def check_user(conn, un, h_pw):
    try:
        with conn.cursor() as cu:
            query = 'SELECT id FROM users WHERE username = ? AND password = ? LIMIT 1'
            cu.execute(query, (un, h_pw))
            return cu.fetchone()
    except Error as e:
        print(f'An error occurred: {e}')
        return None
```
<br>

3) User Input Validation <br>
User might enter an invalid input sometimes, to prevent it, a validation layer after each input could be useful. <br>
<br>

4) Encryption for Stored Passwords<br>
This is the most important aspect by far. The purpose of the whole program is to store the passwords SECURELY. But, passwords are kept plain now. They have to be encrypted before transferring to DB.<br> "bcrypt" or "scrypt" libraries could be used.<br>
<br>

5) User Messages<br>
Cleare messages would provide clearer and more informative messages throughout the application to the end user.<br>
<br>

6) A Logging System (Optional)<br>
For such a simple program like this, a logging system may be unnecessary. However, it can be implemented for hands-on experience.<br>
<br>

7) OOP<br>
For now, program is built upon functions. Better approach would be using OOP principles. Instead of functions, treating each trait of the program as object might beneficial for future. 
<br>

8) Better Naming Convention<br>
Name of the functions and variables should be reviewed and more appropriate and descriptive names should selected.<br>
<br>

9) Error Handling<br>
This one can be combined with logging system.<br>

```
def safe_execute(query, params=()):
    try:
        with conn.cursor() as cu:
            cu.execute(query, params)
            return cu
    except Error as e:
        logging.error(f'An error occurred: {e}')
        return None
```
<br>

10) Advanced Security<br>
"pycryptodome" library is worth to look at for advanced password encryption for future.<br><br><br><br>