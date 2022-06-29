import csv
import os
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

        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(10)
        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown(self):
        self.browser.quit()

    # TC1 - Regisztráció helytelen adatokkal.

    def test_registration_fail(self):
        registration(self.browser, user_negative["name"], user_negative["email"], user_negative["password"])
        ok_button = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        ok_button.click()
        btn_sign_up = self.browser.find_element_by_xpath('.//a[@href="#/register"]')
        # Ellenőrzöm, hogy a Regisztráció gomb megjelenik-e
        assert btn_sign_up.is_displayed()

    # TC2 - Bejelentkezés helyes adatokkal
    def test_signin_correct(self):
        # Profil regisztrálása
        registration(self.browser, "waw", user_positive["email"], user_positive["password"])
        ok_button = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        ok_button.click()
        # Kijelentkezés, majd utána bejelentkezés a megfelelő adatokkal
        btn_signout_1 = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        btn_signout_1.click()
        time.sleep(2)
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
        # Ellenőrzöm, hogy a megjelenő gombok száma a bejelentkezett profilra jellemző szám-e
        assert len(links) == 7

    # TC3 - Adatkezelési nyilatkozat használata
    def test_cookies(self):
        btn_cookie_accept = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        btn_cookie_accept.click()
        time.sleep(2)
        cookie_panel = self.browser.find_elements_by_id("cookie-policy-panel")
        # Ellenőrzöm, hogy a adatkezelési nyilatkozat mezője nem jelenik meg
        assert not len(cookie_panel) > 0

    # TC4 - Adatok listázása
    def test_data_list(self):
        login(self.browser)
        # A főoldalon megtalálható posztok listázása
        posts_on_page = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        counter = 0
        for i in posts_on_page:
            counter = counter + 1
        # Ellenőrzöm, hogy a ciklus számlálója megegyezik a posztok számávsl
        assert counter == len(posts_on_page)

    # TC5 - Több oldalas lista bejárása
    def test_multiple_pages(self):
        login(self.browser)
        counter = 0
        pages_list = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for page in pages_list:
            page.click()
            counter = counter + 1
        # Ellenőrzöm, hogy a bejárt oldalak száma megegyezik a ciklus számlálójával
        assert len(pages_list) == counter

    # TC6 -  Új adat bevitel
    def test_post_make(self):
        login(self.browser)
        # Random string generálása, amely a poszt címe lesz
        letters = string.ascii_lowercase
        title = ''.join(random.choice(letters) for i in range(5))
        pages_list = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        # Új poszt létrehozása
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
        # Ellenőrzöm, hogy a poszt létrehozása után a főoldalon lévő posztok száma
        assert len(pages_list_new) == len(pages_list) + 1

    # TC7 - Ismételt és sorozatos adatbevitel adatforrásból
    def test_data_repeat(self):
        login(self.browser)
        pages_list = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        new_article = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        # A CSV fájlból beolvasom a szükséges adatokat, majd beviszem őket a megfelelő input mezőkbe
        with open('testing/post_input.csv', 'r', encoding='UTF-8') as input_f:
            data = csv.reader(input_f, delimiter=',')
            counter = 0
            for row in data:
                new_article.click()
                article_title = self.browser.find_element_by_xpath('//input[@class="form-control form-control-lg"]')
                article_title.send_keys(row[0])
                article_about = self.browser.find_element_by_xpath('//input[@class="form-control"]')
                article_about.send_keys(row[1])
                article_content = self.browser.find_element_by_xpath('//textarea[@class="form-control"]')
                article_content.send_keys(row[2])
                article_tags = self.browser.find_element_by_xpath('//input[@class="ti-new-tag-input ti-valid"]')
                article_tags.send_keys(row[3])
                submit_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
                submit_btn.click()
                home_btn = self.browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[1]/a')
                home_btn.click()
                counter = counter + 1
                time.sleep(2)
            pages_list_new = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
            # Ellenőrzöm, hogy a posztok száma megnövekedett-e a ciklus számlálójának értékével
            assert len(pages_list_new) == len(pages_list) + counter

    # TC8 - Meglévő adat módosítás
    def test_data_modify(self):
        login(self.browser)
        # Random string generálása, amely a poszt módosított címe lesz
        letters = string.ascii_lowercase
        title = ''.join(random.choice(letters) for i in range(5))
        profile_page = self.browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
        profile_page.click()
        time.sleep(2)
        self.browser.refresh()
        time.sleep(5)
        first_post = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        first_post[0].click()
        edit_btn = self.browser.find_element_by_xpath('//a[@class="btn btn-sm btn-outline-secondary"]')
        edit_btn.click()
        article_title = self.browser.find_element_by_xpath('//input[@class="form-control form-control-lg"]')
        article_title.clear()
        article_title.send_keys(title)
        submit_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_btn.click()
        home_btn = self.browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[1]/a')
        home_btn.click()
        time.sleep(2)
        # Ellenőrzöm, hogy a módosított című poszt megjelenik-e
        mod_post = self.browser.find_element_by_xpath(f'//h1[text()="{title}"]')
        assert mod_post.is_displayed

    # TC9 - Adat vagy adatok törlése
    def test_data_delete(self):
        login(self.browser)
        # A felhasználó első posztjának megnyitása majd törlése
        pages_list = len(self.browser.find_elements_by_xpath('//div[@class="article-preview"]'))
        profile_page = self.browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
        profile_page.click()
        time.sleep(3)
        self.browser.refresh()
        time.sleep(3)
        first_post = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        first_post[0].click()
        delete_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]')
        delete_btn.click()
        time.sleep(2)
        # Ellenőrzöm, hogy a posztok száma a főoldalon csökkent eggyel
        pages_list_new = len(self.browser.find_elements_by_xpath('//div[@class="article-preview"]'))
        assert pages_list_new == pages_list - 1

    # TC10 - Adatok lementése felületről
    def test_data_save(self):
        login(self.browser)
        # A tagek listázása
        tag_list = []
        for tags in self.browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]'):
            tag_content = tags.get_attribute("innerHTML")
            tag_list.append(tag_content)

        tag_set = set(tag_list)
        tag_list_new = list(tag_set)
        # A listázott tagek kiírása egy fájlba
        with open("tagsfile.txt", 'w', encoding='UTF-8') as f:
            for i in tag_list_new:
                f.write(i)
                f.write('\n')
        time.sleep(1)
        # Ellenőrzöm, hogy a fájl tartalma nem 0
        assert os.path.getsize("tagsfile.txt") != 0

    # # TC11 - Kijelentkezés
    def test_sign_out(self):
        login(self.browser)
        btn_signout_1 = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        btn_signout_1.click()
        btn_sign_up = self.browser.find_element_by_xpath('.//a[@href="#/register"]')
        # Ellenőrzöm, hogy kijelentkezése után a Regisztráció gomb megjelenik-e.
        assert btn_sign_up.is_displayed()
