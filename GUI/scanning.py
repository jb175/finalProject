from tkinter import Frame, Label, Entry, Button, Text

import os
import threading
import socket


class Scanning(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="URL:").pack()
        self.url_entry = Entry(self)
        self.url_entry.pack()
        self.url_entry.insert("insert", "localhost")

        self.result_text = Text(self)
        self.result_text.pack()

        Button(self, text="Launch the scanning", command=self.launch_scanning).pack()

    def launch_scanning(self):
        thread = threading.Thread(target=lambda: self.scanning())
        thread.start()

    def scanning(self):

        self.result_text.delete('1.0', 'end')

        self.result_text.insert('end', "---- START ----\n\n")

        directory_path = os.path.dirname(os.path.realpath(__file__))

        ports_path = os.path.join(directory_path, '../Resources/Port Scan/ports.txt')

        with open(ports_path, 'r') as f:
            ports = [line.strip() for line in f]

        open_ports_counter = 0
        closed_ports_counter = 0

        for port in ports:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.settimeout(1)
            result = socket_.connect_ex((self.url_entry.get(), int(port)))

            if result == 0:
                message = "open"
                open_ports_counter += 1
            else:
                message = "closed"
                closed_ports_counter += 1

            socket_.close()

            self.result_text.insert('end', f"{port} is {message}\n")

        self.result_text.insert('end', f"\nSummary:\n - Open ports: {open_ports_counter}\n - Closed ports: {closed_ports_counter}\n")
        self.result_text.insert('end', "\n---- END ----")
