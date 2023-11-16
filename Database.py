import sqlite3
import re

with sqlite3.connect("UserTable.db") as db:
    UserTable = db.cursor()

    UserTable.execute('''
    CREATE TABLE IF NOT EXISTS UserTable(
    userID INTEGER PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    email_address VARCHAR(50) NOT NULL);
    ''')

def RegisterUser(Credentials):

    with sqlite3.connect("UserTable.db") as db:
        cursor = db.cursor()

    find_user = ("SELECT * FROM UserTable WHERE username = ?")
    cursor.execute(find_user, [(Credentials.username.get())])

    if (cursor.fetchall()):
        Credentials.username_error_message.set("Username taken")
        return False

    insert = "INSERT INTO UserTable(username, password, email_address) VALUES(?,?,?)"
    cursor.execute(insert, [(Credentials.username.get()), (Credentials.password.get()), (Credentials.email.get())])
    db.commit()
    return True

def LoginUser(Credentials):

    with sqlite3.connect("UserTable.db") as db:
        cursor = db.cursor()

    if re.match("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$", Credentials.username.get()):
        statement = "SELECT username from UserTable WHERE email_address= ? AND password = ?"
        cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))

    else:
        statement = "SELECT username from UserTable WHERE username= ? AND password = ?"
        cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))

    if not cursor.fetchone():  # An empty result evaluates to False.
        return False

    else:
        return True