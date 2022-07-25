from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import settings

def create_chrome_drive(*,headless=False):
    options=Options()
    if headless:
        options.add_argument("--headless")
    options.add_experimental_option("useAutomationExtension",False)
    options.add_experimental_option('excludeSwitches',['enable-automation'])
    options.add_experimental_option('detach',True)
    web = Chrome(r"C:\Users\LUISLIU1\OneDrive - Schenker AG\Google\Chrome\Application\chromedriver.exe",options=options)
    web.implicitly_wait(10)
    return web

def log_in(url):
    web.get(url)
    web.maximize_window()
    web.find_element(By.CSS_SELECTOR,'#loginUserId').clear()
    web.find_element(By.CSS_SELECTOR,'#loginUserId').send_keys(settings.user_id)
    web.find_element(By.CSS_SELECTOR,'#loginPassword').clear()
    web.find_element(By.CSS_SELECTOR,'#loginPassword').send_keys(settings.password,Keys.ENTER)
    # sleep(3)
    # web.find_element(By.CSS_SELECTOR,'#N1006A').click()
    # pass

def check_12hours_failures():
    find_button=web.find_element(By.CSS_SELECTOR,'#img-navMenuN10016')
    ActionChains(web).move_to_element(find_button).perform()
    # web.find_element(By.CSS_SELECTOR,'#/ui/messages/GetSavedMessageQueryAction?search=Failed+messages-last+12+hours').click()
    web.find_element(By.XPATH,'//*[@href="/ui/messages/GetSavedMessageQueryAction?search=Failed+messages-last+12+hours"]').click()
    single_page_scrolling()

def check_Cisco_inbound():
    web.find_element(By.CSS_SELECTOR, 'form>span:nth-child(10)>a').click()
    web.find_element(By.CSS_SELECTOR, '#senderPartyName').send_keys(settings.from_id)
    web.find_element(By.CSS_SELECTOR,
                     '#field > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(1) > input[type=radio]').click()
    web.find_element(By.CSS_SELECTOR, 'form>span:nth-child(4)>a').click()
    single_page_scrolling()

def single_page_scrolling():
    js="window.scrollBy(0,500)"
    js_top="window.scrollTo(0,-document.body.scrollHeight)"
    for i in range(2):
        sleep(3)
        web.execute_script(js)
    sleep(3)
    web.execute_script(js_top)

def choose_checkstream():
    print(settings.choose_steam)
    choice = input().lower()
    print("You are going to check stream: " + settings.steams_dict[f"{choice}"] + " in 2 seconds!")
    print("3...")
    sleep(1)
    print("2...")
    sleep(1)
    print("1...")
    sleep(1)
    url = settings.message_tracker_dict[f"{choice}"]
    return url

if __name__ == '__main__':

    'function no need right now'
    #choose the steam you wan to check
    url=choose_checkstream()

    # create web driver
    web=create_chrome_drive()

    # stream to check:
    # url="https://b2bi8-sword.dc.signintra.com/ui/"
    # url="https://b2bi2-sword.dc.signintra.com/ui/"

    # log in
    log_in(url)

    # check failures last 12 hours
    check_12hours_failures()

    # check Cisco inbound messages last 1 hour
    if url == "https://b2bi2-sword.dc.signintra.com/ui/":
        check_Cisco_inbound()
    'loop function. 25 times one shift'
    # for count in range(25):
    #     # create web driver
    #     web=create_chrome_drive()
    #
    #     # stream to check:
    #     url="https://b2bi8-sword.dc.signintra.com/ui/"
    #
    #     # log in
    #     log_in(url)
    #
    #     # check failures last 12 hours
    #     check_12hours_failures()
    #
    #     # check Cisco inbound messages last 1 hour
    #     check_Cisco_inbound()
    #
    #     sleep(180)
    #     web.quit()
    #     sleep(1020)



