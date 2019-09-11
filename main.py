# Author: github.com/iDustBin
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import csv
import string
from bs4 import BeautifulSoup
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import re
import pandas as pd
import os
import time
import requests
import base64
from threading import Thread
import json

PROXY = "139.59.143.247:3129"

USER_AGENT = (

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
    'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'
)

FIRST_NAMES=(
    'Lukas',
    'Herold',
    'Gerrit',
    'Justin',
    'Reiner',
    'Rainer',
    'Karl',
    'Adolf',
    'Juergen',
    'Tom',
    'Berry',
    'Karlos',
    'Sebastian',
    'Heinrich'
)

LAST_NAMES=(
    'Kaufmann',
    'Baumhaus',
    'Kleinbielen',
    'Heinzmann',
    'Angular',
    'Oezdemir',
    'Cox',
    'Bode',
    'Schmidt',
    'Heinzelmann'
)

STREETS=(
    'Ackerweg.',
    'Muehlenstr.',
)

ZIP_CODES=(
    ['47608','Geldern'],
    ['40882','Ratingen'],
    ['50213','Koeln'],
    ['50213','Koeln'],
    ['40213','Duesseldorf'],
    ['40873','Duisburg'],
)

api_key = ''
site_key = ''


class Register(Thread):
    
    def run(self):
        self.start_process()
        
    def __init__(self):
        self.passwordLength = 16
        self.client = AnticaptchaClient(api_key)
        self.create_random_value()
        Thread.__init__(self)

    def create_random_value(self):
        self.PHONENUMBER = '128372132'
        self.RECOVERY_EMAIL = 'conf-email@email.com'        
        self.ACTION_URI = 'https://registrierung.gmx.net/#.pc_page.homepage.index.loginbox_1.registrierung'
        self.FIRST_NAME = random.choice(FIRST_NAMES)
        self.LAST_NAME = random.choice(LAST_NAMES)
        self.EMAIL_ADDR = str(self.FIRST_NAME) + str(self.LAST_NAME) 
        self.ZIP_CODE = random.choice(ZIP_CODES)[0]
        self.CITY = random.choice(ZIP_CODES)[1]
        self.STREET = random.choice(STREETS)
        self.BDAY_DAY = random.randint(1, 31)
        self.BDAY_MONTH = random.randint(1, 12)
        self.BDAY_YEAR = random.randint(1988, 1991)
        self.PASSWORD = self.generatedPassword()
        self.CONFIRM_PASSWORD = self.PASSWORD
        # self.PROXY=random.choice(self.get_proxies())
        self.USER_AGENT= random.choice(USER_AGENT)
        self.EMAIL_SUFFIX=''
        self.EMAIL_ALIAS=''

    # def get_proxies(self):
    #     soup = BeautifulSoup(requests.get("http://www.gatherproxy.com/proxylist/country/?c=Germany").text)
    #     #print(soup.text)
    #     proxies=[]
    #     for sc in soup.findAll("script",attrs={"type":"text/javascript"}):
    #         try:
    #                 data = json.loads(str(sc.text[sc.text.find("{"):sc.text.find("}")+1]))
    #                 if data['PROXY_TYPE']=="Elite" and int(data['PROXY_PORT'],16) not in [80,8080]:
    #                         proxies.append(data['PROXY_IP'] + ":" + str(int(data['PROXY_PORT'],16)))
    #         except:
    #                 pass
    #     return proxies

    def find_available_proxy():
        proxies_csv_path = get_full_path("/data/proxies.csv")
        proxies_csv = pandas.read_csv(proxies_csv_path, sep=',', dtype="str")

        # define proxies.csv columns
        proxy_rows = proxies_csv.proxy
        status_rows = proxies_csv.status

        # go through every proxy in .csv and check if it is available to use
        for i, (proxy, status) in enumerate(zip(proxy_rows, status_rows)):
            if i == len(proxy_rows) - 1 and status == "USED":
                print("--------------------------------")
                print("No more proxies!!!")
                print("--------------------------------")
                exit()
            elif pandas.isnull(status):
                proxies_csv.at[i, 'status'] = "USED"
                proxies_csv.to_csv(proxies_csv_path, sep=',', index=False, index_label=False)
            return proxy

    # def generate_random_firstname(self):
    #     with open('names.csv', mode='r') as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=';')
    #         line_count = 0
    #     for row in csv_reader:
    #         first_names = list(csv_reader)
    #         random_first_names = random.choice(first_names)
    #         print(random_first_names)
    #         print(row)
    #     csvFile.close()

    def generatedPassword(self):
        RANDOM_PASSWD = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(RANDOM_PASSWD) for i in range(self.passwordLength))    

    def start_process(self):
        self.PROXY=PROXY
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % self.PROXY)
        chrome_options.add_argument(f'user-agent={USER_AGENT}')
#        chrome_options.add_argument('--headless')
        
        task = webdriver.Chrome("./chromedriver", options=chrome_options)

        # task = webdriver.Remote(
        # command_executor='http://127.0.0.1:4444/wd/hub',
        # options=chrome_options) 
        # task = webdriver.Remote(options=chrome_options)

        task.get(self.ACTION_URI)
        task.implicitly_wait(20)
        task.find_element_by_class_name('pos-form-element').send_keys(self.EMAIL_ADDR)
        
        #time.sleep(10)
        """try:
            task.find_element_by_class_name('pos-form-element').send_keys("self.EMAIL_ADDR2")
            ALIAS_CHECK = task.find_element_by_class_name('pos-input-checkbox__checker')
            ALIAS_CHECK.click()
        except:
            pass"""
        
        task.find_element_by_name('salutation').click()
        task.find_element_by_xpath('//*[@data-test="first-name-input"]').send_keys(self.FIRST_NAME)
        task.find_element_by_xpath('//*[@data-test="last-name-input"]').send_keys(self.LAST_NAME)

        task.find_element_by_xpath('//*[@data-test="postal-code-input"]').send_keys(self.ZIP_CODE)
        task.find_element_by_xpath('//*[@data-test="town-input"]').send_keys(self.CITY)

        task.find_element_by_xpath('//*[@data-test="street-and-number-input"]').send_keys(self.STREET)
        task.find_element_by_xpath('//*[@data-test="day"]').send_keys(str(self.BDAY_DAY))
        task.find_element_by_xpath('//*[@data-test="month"]').send_keys(str(self.BDAY_MONTH))
        task.find_element_by_xpath('//*[@data-test="year"]').send_keys(str(self.BDAY_YEAR))

        task.find_element_by_id('password').send_keys(self.PASSWORD)
        task.find_element_by_id('confirm-password').send_keys(self.CONFIRM_PASSWORD)
#        task.find_element_by_id('mobilePhone').send_keys(str(self.PHONENUMBER))

        task.find_element_by_xpath('/html/body/onereg-app/div[2]/onereg-form/div/div/form/section/section[4]/onereg-password-recovery/fieldset/onereg-progress-meter/div[3]/onereg-checkbox-wrapper/pos-input-checkbox/label/span').click()
        task.find_element_by_xpath('/html/body/onereg-app/div[2]/onereg-form/div/div/form/section/section[4]/onereg-password-recovery/fieldset/onereg-progress-meter/div[4]/onereg-checkbox-wrapper/pos-input-checkbox/label/span').click()
        time.sleep(1)
        task.find_element_by_id('contactEmail').send_keys(self.RECOVERY_EMAIL)        
        image_src = task.find_elements_by_id('captchaImage')[0].get_attribute("src")
        solve_str = self.solve_captcha(image_src)
        task.find_element_by_xpath('//*[@data-test="captcha-input"]').send_keys(str(solve_str))
        task.find_element_by_xpath('//*[@data-test="create-mailbox-create-button"]').click()
        time.sleep(5)
        try:
            self.EMAIL_ALIAS = task.find_elements_by_class_name("onereg-suggestions-box__row")[1].text.split("\n")[0]
            print("alias:" + self.EMAIL_ALIAS)
        except Exception as msg:
            print("alias err:" + str(msg))
        try:
            self.EMAIL_SUFFIX = task.find_element_by_class_name("email-alias-check-select").text.split("\n")[0].strip()
        except:
            pass
        self.save_data()
#        task.find_element_by_xpath('//*[@data-test="create-mailbox-create-button"]').click()
        task.quit()

    def solve_captcha(self, img_base64_str):
        img_base64_str = img_base64_str[img_base64_str.find(",") + 1:]
        imgdata = base64.b64decode(img_base64_str)
        filename = 'captcha_image.jpg'

        with open(filename, 'wb') as f:
            f.write(imgdata)
        captcha_fp = open(filename, 'rb')

        captcha_task = ImageToTextTask(captcha_fp)
        job = self.client.createTask(captcha_task)
        time.sleep(3)
        job.join()
        captcha_solve_str = job.get_captcha_text()
        return captcha_solve_str

    def save_data(self):
        with open('accounts.csv', mode='a') as DATASET:
            COLOUMNS = [ 'PROXY_PROTOCOL','PROXY','EMAIL_ADDR','EMAIL_ALIAS','EMAIL_SUFFIX', 'EMAIL_PASSWD', 'FIRST_NAME', 'LAST_NAME', 'BDAY', 'ZIP_CODE', 'CITY', 'STREET', 'RECOVERY_EMAIL' ]
            WRITER = csv.DictWriter(DATASET, fieldnames=COLOUMNS)
            WRITER.writerow({
                'PROXY_PROTOCOL': "HTTPS",
                'PROXY':str(self.PROXY),
                'EMAIL_ADDR': str(self.EMAIL_ADDR),
                'EMAIL_ALIAS':str(self.EMAIL_ALIAS),
                'EMAIL_SUFFIX': str(self.EMAIL_SUFFIX),
                'EMAIL_PASSWD': self.PASSWORD,
                'FIRST_NAME': str(self.FIRST_NAME), 
                'LAST_NAME': str(self.LAST_NAME), 
                'ZIP_CODE': int(self.ZIP_CODE),
                'CITY': str(self.CITY),
                'STREET': str(self.STREET),
                'RECOVERY_EMAIL': str(self.RECOVERY_EMAIL) 
            })
            DATASET.close()

max_threads=2

if __name__ == '__main__':
    
    for t in range(max_threads):
        t = Register()
        t.start()
