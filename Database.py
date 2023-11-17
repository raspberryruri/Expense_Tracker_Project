import sqlite3
import re
#from tkinter import messagebox as mb
import ttkbootstrap.dialogs.dialogs as mb
import Dashboard

# Initialise User Table
with sqlite3.connect("UserTable.db") as db:
    UserTable = db.cursor()

    UserTable.execute('''
    CREATE TABLE IF NOT EXISTS UserTable(
    userID INTEGER PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    email_address VARCHAR(50) NOT NULL);
    ''')

    db.commit()

# Initialise Expenses Table
with sqlite3.connect("Expense Tracker.db") as db:
    Expenses = db.cursor()

    Expenses.execute(
      'CREATE TABLE IF NOT EXISTS ExpenseTracker '
      '(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
      'Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT, userID INTEGER,'
      'FOREIGN KEY (userID) REFERENCES UserTable(userID))')

    db.commit()
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
        if re.match("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$", Credentials.username.get()):
            statement = "SELECT username from UserTable WHERE email_address= ? AND password = ?"
            cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))
            Credentials.username.set("%s" % cursor.fetchone())

        else:
            statement = "SELECT email_address from UserTable WHERE username= ? AND password = ?"
            cursor.execute(statement, (Credentials.username.get(), Credentials.password.get()))
            Credentials.email.set("%s" % cursor.fetchone())

        return True


def AddExpense(date_var, payee_var, description_var, amount_var, payment_mode_var, table, popup, Visuals):

    if not date_var.get() or not payee_var.get() or not description_var.get() or not amount_var.get() or not payment_mode_var.get():
        mb.Messagebox.ok(title='Fields empty!', message="Please fill all the missing fields before pressing the add button!")

    else:

        with sqlite3.connect("Expense Tracker.db") as db:
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
                # SQL code for inserting values
                (date_var.get(), payee_var.get(), description_var.get(), amount_var.get(), payment_mode_var.get())
                # Parameters to insert into the values in the SQL code
            )
            db.commit()

        popup.destroy()
        Dashboard.UpdateTable(table, Visuals)

def DeleteExpense(values_selected):
    with sqlite3.connect("Expense Tracker.db") as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[
        0])  # SQL code to remove data from ExpenseTracker Table
        db.commit()