import tkinter
import ttkbootstrap as ttk
import Login_Page
import Theme
import Dashboard

# Creates root window
root = tkinter.Tk()
root.withdraw()

# Sets Theme/Fonts
Visuals = Theme.Visuals(style="flatly")

# Login Page Code
Credentials = Login_Page.Credentials()
Login_Page.Login(root, Credentials, Visuals)

# Dashboard Code


root.mainloop()