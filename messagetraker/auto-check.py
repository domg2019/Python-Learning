#  -*- coding: utf-8 -*-
#  Author: luis.liu@dbschenker.com
#  Timestamp for latest update:  7/30/2022  7:54 PM
#  Update: Add some functions to simplify this programming.
#          Add message self-signature so that there is no limitation for receiving messages.


import datetime
from time import sleep
import urllib.request

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from settings import *

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
    web.find_element(By.CSS_SELECTOR,'#loginUserId').send_keys(user_id)
    web.find_element(By.CSS_SELECTOR,'#loginPassword').clear()
    web.find_element(By.CSS_SELECTOR,'#loginPassword').send_keys(password,Keys.ENTER)
    # sleep(3)
    # web.find_element(By.CSS_SELECTOR,'#N1006A').click()
    # pass

def check_12hours_failures():
    find_button=web.find_element(By.CSS_SELECTOR,'#img-navMenuN10016')
    ActionChains(web).move_to_element(find_button).perform()
    # web.find_element(By.CSS_SELECTOR,'#/ui/messages/GetSavedMessageQueryAction?search=Failed+messages-last+12+hours').click()
    web.find_element(By.XPATH,'//*[@href="/ui/messages/GetSavedMessageQueryAction?search=Failed+messages-last+12+hours"]').click()
    single_page_scrolling()

def check_Cisco_12hours_failures():
    web.find_element(By.CSS_SELECTOR, '#senderPartyName').send_keys(from_id)
    web.find_element(By.CSS_SELECTOR, 'form>span:nth-child(4)>a').click()

def Cisco_12hours_failures_handle():
    failure_text = web.find_element(By.XPATH, '//*[@id="queryResults"]/tbody').text.split("\n")
    if failure_text[1] == "The search returned no messages.":
        return f"发送者：{from_id}, 没有进来失败文件."
    else:
        return f"发送者：{from_id}, 有{len(failure_text[1:])}个文件失败！"

def check_Cisco_inbound():
    web.find_element(By.CSS_SELECTOR, 'form>span:nth-child(10)>a').click()
    web.find_element(By.CSS_SELECTOR, '#senderPartyName').send_keys(from_id)
    web.find_element(By.CSS_SELECTOR,
                     '#field > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(1) > input[type=radio]').click()
    web.find_element(By.CSS_SELECTOR, 'form>span:nth-child(4)>a').click()
    single_page_scrolling()

def inbound_info_handle():
    inbound_text = web.find_element(By.XPATH, '//*[@id="queryResults"]/tbody').text.split("\n")
    if len(inbound_text[1::20]) == 5:
        return f"一小时内收到进来文件不小于100"
    elif len(inbound_text[1::20]) > 0:
        number = len(inbound_text[1::20])
        return f"一小时内收到进来文件不小于f{4 * number}"
    else:
        return f"一小时内没有文件进来！"

def single_page_scrolling():
    js="window.scrollBy(0,500)"
    js_top="window.scrollTo(0,-document.body.scrollHeight)"
    for i in range(2):
        sleep(3)
        web.execute_script(js)
    sleep(3)
    web.execute_script(js_top)

def choose_checkstream():
    print(choose_steam)
    choice = input().lower()
    print("You are going to check stream: " + steams_dict[f"{choice}"] + " in 2 seconds!")
    print("3...")
    sleep(1)
    print("2...")
    sleep(1)
    print("1...")
    sleep(1)
    url = message_tracker_dict[f"{choice}"]
    return url,choice

def send_phonemsg():
    data = urllib.parse.urlencode({'u': phonemessage_user, 'p': phonemessage_password, 'm': phonemessage_phone, 'c': content})
    send_url = phonemessage_smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print (phonemessage_statusStr[the_page],current_time)


if __name__ == '__main__':

    'function no need right now'
    #choose the steam you wan to check
    url,choice=choose_checkstream()


    for i in range(16):
        # create web driver
        web=create_chrome_drive()

        #current time
        current_time = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
        # stream to check:
        # url="https://b2bi8-sword.dc.signintra.com/ui/"
        # url="https://b2bi2-sword.dc.signintra.com/ui/"

        # log in
        log_in(url)
        # check failures last 12 hours
        check_12hours_failures()

        # check Cisco inbound messages last 1 hour
        if choice == "v":
            check_Cisco_12hours_failures()
            failure_content = Cisco_12hours_failures_handle()
            check_Cisco_inbound()
            content = "【luis】" + failure_content + inbound_info_handle() + ": " + current_time
            print(content)
            send_phonemsg()

        web.quit()
        if i != 8:
            sleep(900)




