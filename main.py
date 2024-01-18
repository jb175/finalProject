from tkinter import Tk, Menu
from gui.main_page import MainPage
from gui.test_page import TestPage
from gui.dom_xss_page import DomXssPage

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frames = {}

        for F in (MainPage, TestPage, DomXssPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

        # Create a menu
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Main Page", command=lambda: self.show_frame("MainPage"))
        filemenu.add_command(label="Test Page", command=lambda: self.show_frame("TestPage"))
        filemenu.add_command(label="Dom XSS Page", command=lambda: self.show_frame("DomXssPage"))
        menubar.add_cascade(label="Navigate", menu=filemenu)

        # Display the menu
        self.config(menu=menubar)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

app = Application()
app.mainloop()