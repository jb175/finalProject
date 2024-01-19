from tkinter import Tk, Menu
from GUI.analysis import Analysis
from GUI.scanning import Scanning
from GUI.bruteforce import Bruteforce
from GUI.sql_injection import SQLInjection
from GUI.dom_xss_page import DOMXSS


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frames = {}

        for F in (Analysis, Scanning, Bruteforce, SQLInjection, DOMXSS):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Analysis")

        menubar = Menu(self)

        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Analysis", command=lambda: self.show_frame("Analysis"))
        filemenu.add_command(label="Scanning", command=lambda: self.show_frame("Scanning"))
        filemenu.add_command(label="Bruteforce", command=lambda: self.show_frame("Bruteforce"))
        filemenu.add_command(label="SQL Injection", command=lambda: self.show_frame("SQLInjection"))
        filemenu.add_command(label="DOM XSS", command=lambda: self.show_frame("DOMXSS"))

        menubar.add_cascade(label="Navigate", menu=filemenu)

        self.config(menu=menubar)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
