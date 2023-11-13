import sqlite3

with sqlite3.connect("UserTable.db") as db:
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserTable(
    userID INTEGER PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    email_address VARCHAR(50) NOT NULL);
    ''')

def RegisterUser(Credentials):

    if Credentials.username.get() == "Ruby Rose":
        return

    find_user = ("SELECT * FROM UserTable WHERE username = ?")
    cursor.execute(find_user, [(Credentials.username.get())])

    if (cursor.fetchall()):
        Credentials.username_error_message.set("Username taken")
        return

    insert = "INSERT INTO UserTable(username, password, email_address) VALUES(?,?,?)"
    cursor.execute(insert, [(Credentials.username.get()), (Credentials.password.get()), (Credentials.email.get())])
    db.commit()
    return