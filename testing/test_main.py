import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from functions import *
from data_for_input import *

class TestConduit(object):


    def setup(self):
        browser_options = Options()
        # browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.implicitly_wait(10)
        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown(self):
            self.browser.quit()

#TC1 - Regisztráció helytelen adatokkal

    def ttest_registration_fail(self):
        registration(self.browser, user_negative["name"], user_negative["email"], user_negative["password"])
        failed_result = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        error_type = self.browser.find_element_by_xpath('//div[@class="swal-text"]')
        try:
            assert failed_result.text == "Registration failed!" and error_type.text == "Email must be a valid email. "
            print("A vártnak megfelelő hibaüzenet fogad")
        except AssertionError:
            print("Nem megfelelő hibaüzenet")

#TC2 - Bejelentkezés helyes adatokkal
    def ttest_signin_correct(self):
        btn_sign_in_main = self.browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
        btn_sign_in_main.click()
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        email_input.send_keys(user_positive["email"])
        password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        password_input.send_keys(user_positive["password"])
        btn_sign_in = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        btn_sign_in.click()
        time.sleep(2)
        links = self.browser.find_elements_by_xpath('//li[@class="nav-item"]')
        try:
            assert len(links)==7
            print('Sikeres bejelentkezés')
        except AssertionError:
            print('Nem sikerült bejelentkezni')

#TC3 - Adatkezelési nyilatkozat használata
    def test_cookies(self):
        cookie_msg=self.browser.find_element_by_xpath('//div[@class="cookie__bar__content"]')
        btn_cookie_accept=self.browser.find_element_by_xpath('//*[@id="cookie-policy-panel"]/div/div[2]/button[2]')
        btn_cookie_accept.click()
        try:
            assert not cookie_msg.is_displayed()
            print('Sikeresen kezelte az adatkezelési nyilatkozatot')
        except AssertionError:
            print('Az adatkezelési nyilatkozat már korábban el lett fogadva')

#TC4 -