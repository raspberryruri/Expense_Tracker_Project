import datetime
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import sqlite3

# Backgrounds and Fonts
DataEntryFrameBG = '#29AB87'
ButtonFrameBG = '#00A693'
lbl_font = ('Georgia', 13)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT', 13)

# Function for buttons




# Creating gui window
win = Tk()
win.title('Expense Tracker')
win.geometry('1200x550')
Label(win, text='BUDGET PAGE', font=('OpenSans', 15, 'bold'), bg='Aquamarine').pack(side=TOP, fill=X)
BudgetDataEntryFrame = Frame(win, bg=DataEntryFrameBG)
BudgetDataEntryFrame.place(x=0, y=30, relheight=0.95, relwidth=0.25)
InfoFrame = Frame(win, bg=ButtonFrameBG)
InfoFrame.place(relx=0.25, rely=0.055, relwidth=0.75, relheight=1.5)
budget = DoubleVar()
balance = DoubleVar()
Label(BudgetDataEntryFrame, text='Budget\t:', font=lbl_font, bg=DataEntryFrameBG).place(x=10, y=100)
Entry(BudgetDataEntryFrame, font=entry_font, width=31, textvariable=budget).place(x=10, y=130)
Label(BudgetDataEntryFrame, text='Balance\t:', font=lbl_font, bg=DataEntryFrameBG).place(x=10, y=230)
Entry(BudgetDataEntryFrame, font=entry_font, width=31, textvariable=balance).place(x=10, y=260)
# Buttons
Button(BudgetDataEntryFrame, text='Insert Budget', command='AddBudget', font=btn_font, width=25,bg='Aquamarine').place(x=10, y=170)
Button(BudgetDataEntryFrame, text='Insert Balance', font=btn_font, width=25, bg='Aquamarine', command='Insert Balance').place(x=10, y=300)
Button(BudgetDataEntryFrame, text='Back', font=btn_font, width=25, bg='Aquamarine', command='Insert Balance').place(x=10, y=350)
# labels to show balance and stuff
Label(InfoFrame, text='Budget:', font=lbl_font, bg='White').place(x=50, y=70)
Label(InfoFrame, text='Balance:', font=lbl_font, bg='White').place(x=50, y=220)
Label(InfoFrame, text='Remaining Balance:', font=lbl_font, bg='White').place(x=50, y=370)


win.mainloop()