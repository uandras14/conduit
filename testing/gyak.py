from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
import string
from functions import *

browser_options = Options()

browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
browser.implicitly_wait(10)
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

login(browser)
letters = string.ascii_lowercase
title = ''.join(random.choice(letters) for i in range(5))
profile_page = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
profile_page.click()
time.sleep(2)
profile_page.click()
time.sleep(5)
first_post = browser.find_elements_by_xpath('//div[@class="article-preview"]')
first_post[0].click()
edit_btn = browser.find_element_by_xpath('//a[@class="btn btn-sm btn-outline-secondary"]')
edit_btn.click()
article_title = browser.find_element_by_xpath('//input[@class="form-control form-control-lg"]')
article_title.clear()
article_title.send_keys(title)
submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')
submit_btn.click()
home_btn = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[1]/a')
home_btn.click()
time.sleep(2)
mod_post=browser.find_element_by_xpath(f'//h1[text()="{title}"]')
assert not mod_post.is_displayed
