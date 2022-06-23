import time

def login(browser):
    login_button = browser.find_element_by_xpath('//a[@href="#/login"]')
    login_button.click()
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    password_input = browser.find_element_by_xpath('//input[@type="password"]')
    sign_in_button = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    email_input.send_keys('theawnedfisherman@gmail.com')
    password_input.send_keys('qwertzuI1')
    sign_in_button.click()
    time.sleep(5)

def registration(browser, name, email, password):
    sign_up_btn = browser.find_element_by_xpath('//a[@href="#/register"]')
    sign_up_btn.click()
    name_input = browser.find_element_by_xpath('//input[@placeholder="Username"]')
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
    sign_up_send_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    name_input.send_keys(name)
    email_input.send_keys(email)
    password_input.send_keys(password)
    sign_up_send_btn.click()

