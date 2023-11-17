import tkinter
import ttkbootstrap as ttk

class Visuals():

    def __init__(self, style=None):
       self.Theme = ttk.Style(theme=style)
       self.BoldText = tkinter.font.Font(family="Yuanti TC", name="appBoldTextFont", size=30, weight="bold")
       self.BigText = tkinter.font.Font(family="Yuanti TC", name="appBigTextFont", size=24, weight="normal")
       self.Text = tkinter.font.Font(family="Yuanti TC", name="appTextFont", size=12, weight="normal")
       self.Theme.configure("TButton", font=self.Text, fg="black")
       self.Theme.configure("TCheckbutton", font=self.Text, fg="black")
       self.Header = tkinter.font.Font(family="BM Hanna Pro", name="appHeaderFont", size=48, weight="bold")
       self.Error_Text = tkinter.font.Font(family="Yuanti TC Italic", name="appErrorTextFont", size=11, slant="italic")
