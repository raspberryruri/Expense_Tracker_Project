import sqlite3
import tkinter
import ttkbootstrap as ttk
import ttkbootstrap.dialogs.dialogs as dialogs

import Database
import Theme
from datetime import datetime, timedelta

class Dashboard():

    def __init__(self, root, Visuals, Credentials=None):

        # Class Attributes
        self.root = root
        self.Visuals = Visuals
        self.username = "Ruri"
        self.email = "raspberryruri@gmail.com"

        # Update the StringVar values if Credentials is provided
        if Credentials:
            self.username = Credentials.username.get()
            self.email = Credentials.email.get()

        # Creates TopLevel Window
        self.TopLevel = tkinter.Toplevel(self.root)
        self.TopLevel.title("ExpenseMate")
        self.TopLevel.columnconfigure(0, weight=1)
        self.TopLevel.columnconfigure(1, weight=5)
        self.TopLevel.rowconfigure(0, weight=1)
        self.TopLevel.rowconfigure(1, weight=5)

    def Create_Dashboard(self):

        # Creates Left Frame
        FrameW = ttk.Frame(self.TopLevel)
        FrameW.grid(column=0, row=0, rowspan=2, sticky="nwes")

        # ExpenseMate
        ttk.Label(FrameW, text="ExpenseMate", font=self.Visuals.BigText, anchor="center").grid(row=1, column=1, sticky="nwes")

        # Separator
        ttk.Separator(FrameW).grid(row=2, column=1, sticky="nwe")

        # Username (Change)
        ttk.Label(FrameW, text=self.username, font=self.Visuals.BigText, anchor="center").grid(row=3, column=1, sticky="wes")

        # Email (Change)
        ttk.Label(FrameW, text=self.email, font=self.Visuals.Text, anchor="center").grid(row=4, column=1, sticky="nwe")

        # Budget Button
        ttk.Button(FrameW, text="Budget", bootstyle="link").grid(row=5, column=1)

        # Resizing
        FrameW.rowconfigure(0, weight=0)
        FrameW.rowconfigure(1, weight=1)
        FrameW.rowconfigure(2, weight=1)
        FrameW.rowconfigure(3, weight=1)
        FrameW.rowconfigure(4, weight=1)
        FrameW.rowconfigure(5, weight=1)
        FrameW.rowconfigure(6, weight=1)
        FrameW.columnconfigure(1, weight=1)


        # Creates Top Right Frame
        FrameNE = ttk.Frame(self.TopLevel, bootstyle="light")
        FrameNE.grid(column=1, row=0, sticky="nwes")

        # Date
        current_date = datetime.now()
        ttk.Label(FrameNE,anchor="center", text= f"{current_date.strftime('%B %d')}", font=self.Visuals.BoldText, background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=1, sticky="s")
        first_day = current_date.replace(day=1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1))
        daterange = f"{first_day.strftime('%d')} - {last_day.strftime('%d %B, %Y')}"
        ttk.Label(FrameNE, text=daterange, font=self.Visuals.Text, background=self.Visuals.Theme.colors.get("light")).grid(row=2, column=1)

        # Expenses
        ttk.Label(FrameNE, text="Expenses", font=self.Visuals.BoldText, anchor="center", background=self.Visuals.Theme.colors.get("light")).grid(row=1, column=3, columnspan=3, sticky="swe")

        # Edit Expense Button
        ttk.Button(FrameNE, style="primary-outline", text="Edit Expense",
                   command=lambda: EditExpense(self.TopLevel, table, self.Visuals)).grid(row=2, column=3)

        # Delete Expense Button
        ttk.Button(FrameNE, style="primary-outline", text="Delete Expense",
                   command=lambda: DeleteExpense(table, self.Visuals)).grid(row=2, column=4)

        # Add Expense Button
        ttk.Button(FrameNE, style="primary-outline", text="Add Expense", command=lambda: AddExpense(self.TopLevel, table, self.Visuals)).grid(row=2, column=5)

        FrameNE.rowconfigure(1, weight=1)
        FrameNE.rowconfigure(2, weight=1)
        FrameNE.columnconfigure(1, weight=1)
        FrameNE.columnconfigure(2, weight=4)
        FrameNE.columnconfigure(3, weight=1)
        FrameNE.columnconfigure(4, weight=0)
        FrameNE.columnconfigure(5, weight=1)

        # Creates Bottom Right Frame
        FrameSE = ttk.Frame(self.TopLevel, bootstyle="light")
        FrameSE.grid(column=1, row=1, sticky="nwes")

        # Creates Table
        columns = ('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment')
        table = ttk.Treeview(FrameSE, show="headings", columns=columns, bootstyle="info")
        table.grid(row=1, column=1, sticky="nwes")

        # Inserts Table Headings
        table.heading('ID', text='ID No.', anchor="center")
        table.heading('Date', text='Date', anchor="center")
        table.heading('Payee', text='Payee', anchor="center")
        table.heading('Description', text='Description', anchor="center")
        table.heading('Amount', text='Amount', anchor="center")
        table.heading('Mode of Payment', text='Mode of Payment', anchor="center")

        # Creates Scrollbar
        Y_Scroller = ttk.Scrollbar(FrameSE, orient="vertical", command=table.yview, bootstyle="secondary-round")
        Y_Scroller.grid(row=1, column=2, sticky="ns")
        table.config(yscrollcommand=Y_Scroller.set)

        FrameSE.rowconfigure(1, weight=1)
        FrameSE.columnconfigure(1, weight=1)

        UpdateTable(table, self.Visuals)

def UpdateTable(table, Visuals):

    # Resets the Table
    table.delete(*table.get_children())

    # Fetches Data from Database
    with sqlite3.connect("Expense Tracker.db") as db:
        all_data = db.execute('SELECT * FROM ExpenseTracker')
    data = all_data.fetchall()

    # Inserts Data into Table
    for values in data:
        table.insert("", tkinter.END, values=values)

    # Center align specific columns (adjust column indexes accordingly)
    center_aligned_columns = [0, 1, 2, 3, 4, 5]
    for col in center_aligned_columns:
        table.column(table['columns'][col], anchor='center')


def AddExpense(master, table, Visuals):
    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(master)
    popup.title("Add Expense")

    # Make the pop-up window transient for the main window
    popup.transient(master)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    date_var = tkinter.StringVar()
    payee_var = tkinter.StringVar()
    description_var = tkinter.StringVar()
    amount_var = tkinter.StringVar()
    payment_mode_var = tkinter.StringVar()

    # Labels and Entries
    ttk.Label(popup, text="Date:").grid(row=0, column=0, padx=10, pady=5)
    date_entry = ttk.DateEntry(popup, firstweekday=0)
    date_entry.entry.configure(textvariable = date_var)
    date_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Payee:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=payee_var)
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_entry = ttk.Entry(popup, textvariable=description_var)
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = ttk.Entry(popup, textvariable=amount_var)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Mode of Payment:").grid(row=4, column=0, padx=10, pady=5)
    payment_mode_entry = ttk.Combobox(popup, textvariable=payment_mode_var, values=["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"])
    payment_mode_entry.set("Select an item")
    payment_mode_entry.grid(row=4, column=1, padx=10, pady=5)

    payment_mode_entry.bind("<FocusOut>", lambda event, x=payment_mode_var:validate_input(event, x))

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit", command=lambda: Database.AddExpense(date_var, payee_var, description_var, amount_var, payment_mode_var, table, popup, Visuals))
    submit_button.grid(row=5, column=1, pady=10)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(0, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)
    popup.rowconfigure(3, weight=1)
    popup.rowconfigure(4, weight=1)
    popup.rowconfigure(5, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    master.wait_window(popup)

def EditExpense(master, table, Visuals):
    selected_item = table.selection()
    if not selected_item:
        dialogs.Messagebox.ok(title="Error", message="Please select an expense to edit.")
        return

    # Get values from the selected row
    item_values = table.item(selected_item)['values']

    # Create a Toplevel window for the pop-up
    popup = ttk.Toplevel(master)
    popup.title("Edit Expense")

    # Make the pop-up window transient for the main window
    popup.transient(master)

    # Make the pop-up window grab the focus
    popup.grab_set()

    # StringVars for user inputs
    id = item_values[0]
    date_var = tkinter.StringVar(value=item_values[1])
    payee_var = tkinter.StringVar(value=item_values[2])
    description_var = tkinter.StringVar(value=item_values[3])
    amount_var = tkinter.StringVar(value=item_values[4])
    payment_mode_var = tkinter.StringVar(value=item_values[5])

    # Labels and Entries
    ttk.Label(popup, text="Date:").grid(row=0, column=0, padx=10, pady=5)
    date_entry = ttk.DateEntry(popup, firstweekday=0)
    date_entry.entry.configure(textvariable = date_var)
    date_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Payee:").grid(row=1, column=0, padx=10, pady=5)
    payee_entry = ttk.Entry(popup, textvariable=payee_var)
    payee_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_entry = ttk.Entry(popup, textvariable=description_var)
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
    amount_entry = ttk.Entry(popup, textvariable=amount_var)
    amount_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(popup, text="Mode of Payment:").grid(row=4, column=0, padx=10, pady=5)
    payment_mode_entry = ttk.Combobox(popup, textvariable=payment_mode_var, values=["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"])
    payment_mode_entry.set("Select an item")
    payment_mode_entry.grid(row=4, column=1, padx=10, pady=5)

    payment_mode_entry.bind("<FocusOut>", lambda event, x=payment_mode_var:validate_input(event, x))

    # Button to submit the form
    submit_button = ttk.Button(popup, text="Submit", command=lambda: Database.EditExpense(date_var, payee_var, description_var, amount_var, payment_mode_var, table, popup, Visuals, id))
    submit_button.grid(row=5, column=1, pady=10)

    # Resizes
    popup.columnconfigure(0, weight=1)
    popup.columnconfigure(1, weight=1)
    popup.rowconfigure(0, weight=1)
    popup.rowconfigure(1, weight=1)
    popup.rowconfigure(2, weight=1)
    popup.rowconfigure(3, weight=1)
    popup.rowconfigure(4, weight=1)
    popup.rowconfigure(5, weight=1)

    # Wait for the pop-up window to be destroyed before allowing the main window to regain focus
    master.wait_window(popup)

def DeleteExpense(table, Visuals):
    if not table.selection():  # If there is no table selected
        dialogs.Messagebox.ok(title='No record selected!', message='Please select a record to delete!')
        return
    current_selected_expense = table.item(table.focus())  # Set current selected item in table
    values_selected = current_selected_expense[
        'values']  # Selecting the Values needed to be deleted (Which is values)
    surety = dialogs.Messagebox.yesno(title="Delete expense?", message="Action cannot be undone.")
    if surety == "Yes":
        Database.DeleteExpense(values_selected)
    UpdateTable(table, Visuals)
    dialogs.Messagebox.ok(title='Record deleted!', message='The record you wanted to delete has been deleted successfully')

def validate_input(event, textvar):
    selected_item = textvar.get()

    if selected_item not in ["Cash", "Credit Card", "Debit Card", "TNG E-Wallet"]:
        textvar.set("Select an item")





if __name__ == "__main__":

    # Creates root window
    root = tkinter.Tk()
    root.withdraw()

    MainPage = Dashboard(root, Theme.Visuals(style="flatly"))
    MainPage.Create_Dashboard()

    root.mainloop()