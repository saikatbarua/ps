#!/usr/bin/env python

import os
import time
import subprocess
import requests as rq

class Webdriver(object):
    def __init__(self, **args):
        """
        We can provide executable path if we wish
        Args:
            executable_path (str): Path to webdriver executable
        """

        # Host with port that serves data and controls the browser 
        self.host = "http://127.0.0.1:4444"
        # We need to send json data
        self.header = {
            "Content-Type": "application/json"
        }
        # After getting sessionId it will hold that
        self.sessionId = ""

        if args.get('executable_path'):
            subprocess.Popen([args.get('executable_path'), "--port=4444"])
        else:
            driver_path = os.path.join(os.getcwd(), "chromedriver")
            subprocess.Popen([driver_path, "--port=4444"])

        self.get_session()

    def get_session(self):
        """
        Retrieves Session ID
        """

        data = {
            "capabilities": {
                "acceptInsecureCerts": True
            }
        }

        res = rq.post(f"{self.host}/session", json=data, headers=self.header)
        self.sessionId = res.json().get('value').get('sessionId')

    def get(self, url):
        """[summary]
        Args:
            url (str): URL we want to browse
        """

        data = {"url": url}
        rq.post(f"{self.host}/session/{self.sessionId}/url", json=data, headers=self.header)

    def find(self, by, value):
        """
        Finds Elements
        The Elements are:
            id, name, xpath, tag name, css selector, partial link text, link text
        Args:
            by (str): element name
            value (str): Value to search
        Returns:
            [type]: [description]
        """

        data = {"using": by, "value": value}
        res = rq.post(f"{self.host}/session/{self.sessionId}/element", json=data, headers=self.header)
        return list(res.json().get('value').values())[0]

    def quite(self):
        """
        Ends the session
        """
        rq.delete(f"{self.host}/session/{self.sessionId}", headers=self.header)

def main():
    """
    Main Function
    """
    driver = Webdriver()
    url = "https://www.google.com/"
    driver.get(url)
    time.sleep(0.5)
    element_id = driver.find('xpath', '//input[@name="q"]')
    print(element_id)
    sleep(5)
    driver.quite()

if __name__ == "__main__":
    main()
