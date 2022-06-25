from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from functions import *

browser_options = Options()

browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
browser.implicitly_wait(10)
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

login_button = browser.find_element_by_xpath('//a[@href="#/login"]')
login_button.click()
email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
password_input = browser.find_element_by_xpath('//input[@type="password"]')
sign_in_button = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
email_input.send_keys('theawnedfisherman@gmail.com')
password_input.send_keys('qwertzuI1')
sign_in_button.click()
time.sleep(5)
posts_on_page = browser.find_elements_by_xpath('//div[@class="article-preview"]')
ez=posts_on_page[10].get_attribute("href")
print(ez)
print(len(posts_on_page))
