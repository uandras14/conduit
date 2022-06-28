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

login(browser)
tag_list=[]
for tags in browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]'):
    tag_content=tags.get_attribute("innerHTML")
    tag_list.append(tag_content)


tag_set=set(tag_list)
tag_list_new=list(tag_set)
print(tag_list_new)
# letters = string.ascii_lowercase
# title = ''.join(random.choice(letters) for i in range(5))
# profile_page = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
# profile_page.click()
# time.sleep(2)
# profile_page.click()
# time.sleep(5)
# first_post = browser.find_elements_by_xpath('//div[@class="article-preview"]')
# first_post[0].click()
# edit_btn = browser.find_element_by_xpath('//a[@class="btn btn-sm btn-outline-secondary"]')
# edit_btn.click()
# article_title = browser.find_element_by_xpath('//input[@class="form-control form-control-lg"]')
# article_title.clear()
# article_title.send_keys(title)
# submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')
# submit_btn.click()
# home_btn = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[1]/a')
# home_btn.click()
# time.sleep(2)
# mod_post = browser.find_element_by_xpath(f'//h1[text()="{title}"]')
# assert not mod_post.is_displayed

# login(browser)
# pages_list = len(browser.find_elements_by_xpath('//div[@class="article-preview"]'))
# profile_page = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
# profile_page.click()
# time.sleep(3)
# browser.refresh()
# time.sleep(3)
# first_post = browser.find_elements_by_xpath('//div[@class="article-preview"]')
# first_post[0].click()
# delete_btn = browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]')
# delete_btn.click()
# time.sleep(2)
# pages_list_new = len(browser.find_elements_by_xpath('//div[@class="article-preview"]'))
# print(pages_list_new)
# print(pages_list)
