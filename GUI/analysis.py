from tkinter import Frame, Label, Entry, Button, Text
from bs4 import BeautifulSoup

import requests
import threading


def get_domain(url):
    return url.split('/')[2]


def absence_of_anti_csrf_token_check(text):
    return not (text and ('token' in text or 'csrf' in text))


class Analysis(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="URL:").pack()
        self.url_entry = Entry(self)
        self.url_entry.pack()
        self.url_entry.insert("insert", "http://localhost:3000")

        self.result_text = Text(self)
        self.result_text.pack()

        Button(self, text="Launch the analysis", command=self.launch_analysis).pack()

    def launch_analysis(self):

        thread = threading.Thread(target=lambda: self.analysis())
        thread.start()

    def analysis(self):

        self.result_text.delete('1.0', 'end')
        self.result_text.insert('end', "---- START ----\n\n")

        alerts_counter = [0, 0, 0]
        alerts_counter = self.cloud_metadata_check(alerts_counter)
        alerts_counter = self.grouped_check(alerts_counter)

        self.result_text.insert('end',
                                f"\nSummary (10 checks):\n - High alerts: {alerts_counter[0]}\n - Medium alerts: {alerts_counter[1]}\n - Low alerts: {alerts_counter[2]}\n")
        self.result_text.insert('end', "\n---- END ----")

    def cloud_metadata_check(self, alerts_counter):

        response = requests.get(self.url_entry.get() + "/latest/meta-data")

        if response.status_code == 200:
            self.result_text.insert('end', "[High] Cloud metadata potentially exposed\n")
            alerts_counter[0] += 1

        return alerts_counter

    def grouped_check(self, alerts_counter):

        response = requests.get(self.url_entry.get())
        headers = response.headers
        html = BeautifulSoup(response.text, 'html.parser')

        alerts_counter = self.csp_header_not_set_check(headers, alerts_counter)
        alerts_counter = self.cross_domain_misconfiguration_check(headers, alerts_counter)
        alerts_counter = self.absence_of_anti_csrf_tokens_check(html, alerts_counter)
        alerts_counter = self.missing_anti_clickjacking_header_check(headers, alerts_counter)
        alerts_counter = self.cross_domain_javascript_file_inclusion_check(html, alerts_counter)
        alerts_counter = self.cookie_no_http_only_flag_check(headers, alerts_counter)
        alerts_counter = self.cookie_with_same_site_attribute_none_check(headers, alerts_counter)
        alerts_counter = self.x_content_type_options_header_missing(headers, alerts_counter)
        alerts_counter = self.strict_transport_security_header_not_set(headers, alerts_counter)
        return alerts_counter

    def csp_header_not_set_check(self, headers, alerts_counter):
        if "Content-Security-Policy" not in headers:
            self.result_text.insert('end', "[Medium] Content Security Policy (CSP) header not set\n")
            alerts_counter[1] += 1
        return alerts_counter

    def cross_domain_misconfiguration_check(self, headers, alerts_counter):
        key = "Access-Control-Allow-Origin"
        if key in headers and headers[key] == "*":
            self.result_text.insert('end', "[Medium] Cross-domain misconfiguration\n")
            alerts_counter[1] += 1
        return alerts_counter

    def absence_of_anti_csrf_tokens_check(self, html, alerts_counter):

        break_other_loop = False

        for form_tag in html.find_all('form'):

            for input_tag in form_tag.find_all('input'):

                input_name = input_tag.get('name').lower()
                input_id = input_tag.get('id').lower()

                input_name_check = absence_of_anti_csrf_token_check(input_name)
                input_id_check = absence_of_anti_csrf_token_check(input_id)

                if input_name_check and input_id_check:
                    self.result_text.insert('end', "[Medium] Absence of anti-CSRF tokens\n")
                    alerts_counter[1] += 1
                    break_other_loop = True
                    break

            if break_other_loop:
                break

        return alerts_counter

    def missing_anti_clickjacking_header_check(self, headers, alerts_counter):
        key = "Content-Security-Policy"
        if (key in headers and headers[key] == "frame-ancestors") or "X-Frame-Options" in headers:
            self.result_text.insert('end', "[Medium] Missing anti-clickjacking header\n")
            alerts_counter[1] += 1
        return alerts_counter

    def cross_domain_javascript_file_inclusion_check(self, html, alerts_counter):

        for script_tag in html.find_all('script', {'src': True}):

            script_source = script_tag['src']

            root_condition = (not script_source.startswith("//")
                              and (script_source.startswith("/")
                                   or script_source.startswith("./")
                                   or script_source.startswith(".//")))

            cross_condition = get_domain(self.url_entry.get()) == get_domain(script_source)

            if not root_condition and not cross_condition:
                self.result_text.insert('end', "[Low] Cross-domain JavaScript source file inclusion\n")
                alerts_counter[2] += 1
                break

        return alerts_counter

    def cookie_no_http_only_flag_check(self, headers, alerts_counter):
        key = "Set-Cookie"
        if key in headers and "httponly" in headers[key]:
            self.result_text.insert('end', "[Low] Cookie no HttpOnly flag\n")
            alerts_counter[2] += 1
        return alerts_counter

    def cookie_with_same_site_attribute_none_check(self, headers, alerts_counter):
        key = "Set-Cookie"
        if key in headers and "samesite=none" in headers[key]:
            self.result_text.insert('end', "[Low] Cookie with SameSite attribute None check\n")
            alerts_counter[2] += 1
        return alerts_counter

    def x_content_type_options_header_missing(self, headers, alerts_counter):
        if "X-Content-Type-Options" not in headers:
            self.result_text.insert('end', "[Low] X-ContentType-Options header missing\n")
            alerts_counter[2] += 1
        return alerts_counter

    def strict_transport_security_header_not_set(self, headers, alerts_counter):
        if "Strict-Transport-Security" not in headers:
            self.result_text.insert('end', "[Low] Strict-Transport-Security header not set\n")
            alerts_counter[2] += 1
        return alerts_counter
