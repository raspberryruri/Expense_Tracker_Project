import tkinter
import ttkbootstrap as ttk

class Dashboard():

    def __init__(self, root, Visuals, *args):

        # Class Attributes
        self.root = root

        self.TopLevel = tkinter.Toplevel(self.root)
        self.TopLevel.title("ExpenseMate")
        self.TopLevel.columnconfigure(0, weight=1)
        self.TopLevel.columnconfigure(1, weight=5)
        self.TopLevel.rowconfigure(0, weight=1)
        self.TopLevel.rowconfigure(1, weight=5)

    def Create_Dashboard(self):

        FrameW = ttk.Frame(self.TopLevel)
        FrameW.grid(column=0, row=0, rowspan=2, sticky="nwes")

        FrameW.rowconfigure(1, weight=1)
        FrameW.columnconfigure(1, weight=1)

        FrameNE = ttk.Frame(self.TopLevel, bootstyle="light")
        FrameNE.grid(column=1, row=0, sticky="nwes")

        FrameSE = ttk.Frame(self.TopLevel, bootstyle="light")
        FrameSE.grid(column=1, row=1, sticky="nwes")

if __name__ == "__main__":

    import Theme

    # Creates root window
    root = tkinter.Tk()
    root.withdraw()

    # Sets Theme/Fonts
    Visuals = Theme.Visuals(style="flatly")

    MainPage = Dashboard(root, Visuals)
    MainPage.Create_Dashboard()

    root.mainloop()