from tkinter import Frame


class Welcome(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
