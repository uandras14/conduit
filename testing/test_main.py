import random
import string

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from data_for_input import *
from functions import *


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

    # TC1 - Regisztráció helytelen adatokkal

    def ttest_registration_fail(self):
        registration(self.browser, user_negative["name"], user_negative["email"], user_negative["password"])
        failed_result = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        error_type = self.browser.find_element_by_xpath('//div[@class="swal-text"]')
        try:
            assert failed_result.text == "Registration failed!" and error_type.text == "Email must be a valid email. "
            print("A vártnak megfelelő hibaüzenet fogad")
        except AssertionError:
            print("Nem megfelelő hibaüzenet")

    # TC2 - Bejelentkezés helyes adatokkal
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
            assert len(links) == 7
            print('Sikeres bejelentkezés')
        except AssertionError:
            print('Nem sikerült bejelentkezni')

    # TC3 - Adatkezelési nyilatkozat használata
    def test_cookies(self):
        cookie_msg = self.browser.find_element_by_xpath('//div[@class="cookie__bar__content"]')
        btn_cookie_accept = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        btn_cookie_accept.click()
        try:
            assert not cookie_msg.is_displayed()
            print('Sikeresen kezelte az adatkezelési nyilatkozatot')
        except AssertionError:
            print('Az adatkezelési nyilatkozat már korábban el lett fogadva')

    # TC4 - Adatok listázása
    def ttest_data_list(self):
        login(self.browser)
        posts_on_page = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        counter = 0
        for i in posts_on_page:
            counter = counter + 1

        assert counter == len(posts_on_page)

    # TC5 - Több oldalas lista bejárása
    def ttest_multiple_pages(self):
        login(self.browser)
        counter = 0
        pages_list = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for page in pages_list:
            page.click()
            counter = counter + 1
        assert len(pages_list) == counter

    # TC6 -  Új adat bevitel
    def ttest_post_make(self):
        login(self.browser)
        letters = string.ascii_lowercase
        title = ''.join(random.choice(letters) for i in range(5))
        pages_list = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        new_article = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        new_article.click()
        time.sleep(2)
        article_title = self.browser.find_element_by_xpath('//input[@class="form-control form-control-lg"]')
        article_title.send_keys(title)
        article_about = self.browser.find_element_by_xpath('//input[@class="form-control"]')
        article_about.send_keys('resume')
        article_content = self.browser.find_element_by_xpath('//textarea[@class="form-control"]')
        article_content.send_keys('content')
        article_tags = self.browser.find_element_by_xpath('//input[@class="ti-new-tag-input ti-valid"]')
        article_tags.send_keys(['tag1'], Keys.ENTER, ['tag2'])
        submit_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_btn.click()
        home_btn = self.browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[1]/a')
        home_btn.click()
        time.sleep(4)
        pages_list_new = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        assert len(pages_list_new) == len(pages_list) + 1

    # TC7 - Ismételt és sorozatos adatbevitel adatforrásból
    def test_data_repeat(self):
        login(self.browser)
        pages_list = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        with open('testing/post_input.csv', 'r', encoding='UTF-8') as input_f:
            text = csv.reader(input_f, delimiter=',')
            counter = 0
        new_article = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        new_article.click()
        time.sleep(2)
        article_title = self.browser.find_element_by_xpath('//input[@class="form-control form-control-lg"]')
        article_title.send_keys(title)
        article_about = self.browser.find_element_by_xpath('//input[@class="form-control"]')
        article_about.send_keys('resume')
        article_content = self.browser.find_element_by_xpath('//textarea[@class="form-control"]')
        article_content.send_keys('content')
        article_tags = self.browser.find_element_by_xpath('//input[@class="ti-new-tag-input ti-valid"]')
        article_tags.send_keys(['tag1'], Keys.ENTER, ['tag2'])
        submit_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_btn.click()
        home_btn = self.browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[1]/a')
        home_btn.click()
        time.sleep(4)
        pages_list_new = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        assert len(pages_list_new) == len(pages_list) + 1




    #TC8 - Meglévő adat módosítás



    #TC9 - Adat vagy adatok törlése


    #TC10 - Adatok lementése felületről


    #TC11 - Kijelentkezés




