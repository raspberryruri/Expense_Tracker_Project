import datetime
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import sqlite3
# Creating Database system
connector = sqlite3.connect("Expense Tracker.db")
cursor = connector.cursor()
connector.execute(
  'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
)
connector.commit()
# Initials
# def MonthyBudget():


# List All Expenses function (Mostly for resetting the table or checking)
def ListAllExpenses():
    global connector, table
    table.delete(*table.get_children()) # Resetting the table first
    all_data = connector.execute('SELECT * FROM ExpenseTracker') # Selecting all from Table
    data = all_data.fetchall() # Fetching the data from the table
    for values in data: # using for loop to list values in table
        table.insert('', END, values=values)

# View Expense Details Function
def ShowExpenseDetails():
    global table
    if not table.selection():
        mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
        return
    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']
    message = f'Expense details: \n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'
    mb.showinfo('Here\'s the expense details', message)
# ResetExpenseDetailsEntry
def ResetExpenseDetailsEntry():
    global table
    global date, payee, desc, amnt, MoP
    if not table.selection():
        mb.showerror('No expense selected', 'Please select an expense from the table to view it\'s details') # Making Message box for error when no expense is picked
        current_selected_expense = table.item(table.focus())
        values = current_selected_expense['values']
        expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
        date.set_date(expenditure_date); payee.set(values[2]); desc.set(values[3]); amnt.set(values[4]); MoP.set(values[5])

# Function to clear all fields (for delete expense and delete all expense usage)
def ClearField():
    global desc, payee, amnt, MoP, date, table
    today_date = datetime.datetime.now().date()
    desc.set(''); payee.set(''); amnt.set(0.0); MoP.set('Cash'), date.set_date(today_date)
    table.selection_remove(*table.selection())

# Remove Expense Function
def RemoveExpense():
    if not table.selection(): # If there is no table selected
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return
    current_selected_expense = table.item(table.focus()) # Set current selected item in table
    values_selected = current_selected_expense['values'] # Selecting the Values needed to be deleted (Which is values)
    surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')
    if surety: # If True
        connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0]) # SQL code to remove data from ExpenseTracker Table
        connector.commit()
        ListAllExpenses() #List out the expenses again to show table empty
        mb.showinfo('Record deleted!', 'The record you wanted to delete has been deleted successfully')

# Removal of all the Table items
def RemoveAllExpenses():
  surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')
  if surety:
     table.delete(*table.get_children()) # Getting the children (tuple that belongs to an item)
     connector.execute('DELETE FROM ExpenseTracker')
     connector.commit()
     ClearField()
     ListAllExpenses()
     mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')

def AddExpense():
  global date, payee, desc, amnt, MoP
  global connector
  if not date.get() or not payee.get() or not desc.get() or not amnt.get() or not MoP.get():
     mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
  else:
     connector.execute(
     'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)', #SQL code for inserting values
     (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get()) #Parameters to insert into the values in the SQL code
     )
     connector.commit()
     ClearField()
     ListAllExpenses()
     mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database.')

def EditExpense():
    global table
    def EditExistingExpense():
        global date, amnt, desc, payee, MoP
        global connector, table
        current_selected_expense = table.item(table.focus())
        contents = current_selected_expense['values']
        connector.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
                       (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get(), contents[0]))
        connector.commit()
        ClearField()
        ListAllExpenses()
        mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
        edit_btn.destroy()
        return
    if not table.selection():
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
        return
    ResetExpenseDetailsEntry()
    edit_btn = Button(DataEntryFrame, text='Edit expense', font=btn_font, width=30, bg='Aquamarine', command=EditExistingExpense)
    edit_btn.place(x=10, y=395)

# Backgrounds and Fonts
DataEntryFrameBG = '#29AB87'
ButtonFrameBG = '#00A693'
lbl_font = ('Georgia', 13)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT', 13)

# Creating gui window
win = Tk()
win.title('Expense Tracker')
win.geometry('1200x550')
Main = Frame(win)
Budget = Frame(win)
Label(win, text='EXPENSE TRACKER', font=('OpenSans', 15, 'bold'), bg='Aquamarine').pack(side=TOP, fill=X)
DataEntryFrame = Frame(win, bg=DataEntryFrameBG)
DataEntryFrame.place(x=0, y=30, relheight=0.95, relwidth=0.25)
ButtonFrame = Frame(win, bg=ButtonFrameBG)
ButtonFrame.place(relx=0.25, rely=0.055, relwidth=0.75, relheight=0.30)
InfoFrame = Frame(win)
InfoFrame.place(relx=0.25, rely=0.275, relwidth=0.75, relheight=0.77)
desc = StringVar()
amnt = DoubleVar()
payee = StringVar()
MoP = StringVar(value='Cash')
# Data Entry Frame
Label(DataEntryFrame, text='Date (M/DD/YY) :', font=lbl_font, bg=DataEntryFrameBG).place(x=10, y=50)
date = DateEntry(DataEntryFrame, date=datetime.datetime.now().date(), font=entry_font)
date.place(x=160, y=50)

# Creating gui window for budget
Label(Budget, text='EXPENSE TRACKER', font=('OpenSans', 15, 'bold'), bg='Aquamarine').pack(side=TOP, fill=X)
BudgetDataEntryFrame = Frame(Budget, bg=DataEntryFrameBG)
BudgetDataEntryFrame.place(x=0, y=30, relheight=0.95, relwidth=0.25)
BudgetButtonFrame = Frame(Budget, bg=ButtonFrameBG)
BudgetButtonFrame.place(relx=0.25, rely=0.055, relwidth=0.75, relheight=0.30)
BudgetInfoFrame = Frame(Budget)
BudgetInfoFrame.place(relx=0.25, rely=0.275, relwidth=0.75, relheight=0.77)

Label(DataEntryFrame, text='Payee\t:', font=lbl_font, bg=DataEntryFrameBG).place(x=10, y=230)

Entry(DataEntryFrame, font=entry_font, width=31, textvariable=payee).place(x=10, y=260)
Label(DataEntryFrame, text='Description\t:', font=lbl_font, bg=DataEntryFrameBG).place(x=10, y=100)
Entry(DataEntryFrame, font=entry_font, width=31, textvariable=desc).place(x=10, y=130)
Label(DataEntryFrame, text='Amount\t:', font=lbl_font, bg=DataEntryFrameBG).place(x=10, y=180)
Entry(DataEntryFrame, font=entry_font, width=14, textvariable=amnt).place(x=160, y=180)
Label(DataEntryFrame, text='Mode of Payment:', font=lbl_font, bg=DataEntryFrameBG).place(x=10, y=310)
dd1 = OptionMenu(DataEntryFrame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
dd1.place(x=160, y=305)
dd1.configure(width=10, font=entry_font)
Button(DataEntryFrame, text='Add Expense', command=AddExpense, font=(btn_font, 11,'bold'), width=30,bg='Aquamarine').place(x=10, y=395)

# Buttons
Button(ButtonFrame, text='Delete Expense', font=btn_font, width=25, bg='Aquamarine', command=RemoveExpense).place(x=30, y=5)
Button(ButtonFrame, text='Delete All Expenses', font=btn_font, width=25, bg='Aquamarine', command=RemoveAllExpenses).place(x=335, y=5)
Button(ButtonFrame, text='View Selected Expense\'s Details', font=btn_font, width=25, bg='Aquamarine', command=ShowExpenseDetails).place(x=640, y=5)
Button(ButtonFrame, text='Edit Selected Expense', font=btn_font, width=25, bg='Aquamarine', command=EditExpense).place(x=182.5, y=65)
Button(ButtonFrame, text='Monthly Budget', font=btn_font, width=25, bg='Aquamarine', command='MonthyBudget').place(x=487.5, y=65)

table =ttk.Treeview(InfoFrame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'))
X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)
table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)
table.heading('ID', text='ID No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=95, stretch=NO)  # Date column
table.column('#3', width=150, stretch=NO)  # Payee column
table.column('#4', width=325, stretch=NO)  # Title column
table.column('#5', width=135, stretch=NO)  # Amount column
table.column('#6', width=125, stretch=NO)  # Mode of Payment column
table.place(relx=0, y=0, relheight=1, relwidth=1)

win.mainloop()
