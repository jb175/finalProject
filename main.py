from tkinter import Tk, Menu
from GUI.welcome import Welcome
from GUI.bruteforce import Bruteforce
from GUI.sql_injection import SQLInjection


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frames = {}

        for F in (Welcome, Bruteforce, SQLInjection):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Welcome")

        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Welcome", command=lambda: self.show_frame("Welcome"))
        filemenu.add_command(label="Bruteforce", command=lambda: self.show_frame("Bruteforce"))
        filemenu.add_command(label="SQL Injection", command=lambda: self.show_frame("SQLInjection"))
        filemenu.add_command(label="DOM XSS", command=lambda: self.show_frame(""))
        filemenu.add_command(label="Reflected XSS", command=lambda: self.show_frame(""))
        filemenu.add_command(label="XEE", command=lambda: self.show_frame(""))
        filemenu.add_command(label="SSRF", command=lambda: self.show_frame(""))

        menubar.add_cascade(label="Navigate", menu=filemenu)

        self.config(menu=menubar)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
