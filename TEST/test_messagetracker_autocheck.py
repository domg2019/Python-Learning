#  -*- coding: utf-8 -*-
#####################################################################################
# Author: luis.liu@dbschenker.com
# Message Tracker automated checking, ways: email, phone-message
#
# previous updates:
# 30.08.2022        2h update       fix the bug that mcp 3A/3B can't be checked
# 14.08.2022        1h update       add other two webdriver firefox and edge
# 07.08.2022        2h update       comment out Hypercare functions and add emails function
# 29.07.2022        1h update       add function to send short message
# 24.07.2022        2h ported       first version for checking typical sender 4 times per hour
#####################################################################################


from time import sleep
from datetime import datetime
import urllib.request

import schedule
from selenium.common.exceptions import NoSuchElementException
from win32com import client as win32
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from settings import *

PHONE_NUM = phone_num['luisliu1']


def create_chrome_drive(*, headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('detach', True)
    web_drive = Chrome(r"/Users/LUISLIU1/OneDrive - Schenker AG/Google/Chrome/Application/chromedriver.exe",
                       options=options)
    web.implicitly_wait(10)
    return web_drive


def create_firefox_drive():
    firefox_binary = "/Program Files/Mozilla Firefox/firefox.exe"
    executable_path = "/Users/LUISLIU1/Desktop/python/geckodriver-v0.32.2-win64/geckodriver.exe"
    return webdriver.Firefox(firefox_binary=firefox_binary, executable_path=executable_path)


def create_edge_drive():
    executable_path = "/Users/LUISLIU1/Desktop/python/edgedriver_win64/msedgedriver.exe"
    edge_web = webdriver.Edge(executable_path=executable_path)
    return edge_web


def log_in(url):
    web.get(url)
    web.maximize_window()
    try:
        web.find_element(By.CSS_SELECTOR, '#loginUserId').clear()
    except NoSuchElementException:
        web.find_element(By.CSS_SELECTOR, '#details-button').click()
        web.find_element(By.CSS_SELECTOR, '#proceed-link').click()
        web.find_element(By.CSS_SELECTOR, '#loginUserId').clear()
    web.find_element(By.CSS_SELECTOR, '#loginUserId').send_keys(user_id)
    web.find_element(By.CSS_SELECTOR, '#loginPassword').clear()
    web.find_element(By.CSS_SELECTOR, '#loginPassword').send_keys(password, Keys.ENTER)
    # sleep(3)
    # web.find_element(By.CSS_SELECTOR,'#N1006A').click()
    # pass


def check_12hours_failures():
    try:
        find_button = web.find_element(By.CSS_SELECTOR, '#img-navMenuN10016')
    except NoSuchElementException:
        find_button = web.find_element(By.CSS_SELECTOR, '#img-navMenuN1001B')
    ActionChains(web).move_to_element(find_button).perform()
    web.find_element(By.XPATH,
                     '//*[@href="/ui/messages/GetSavedMessageQueryAction?search=Failed+messages-last+12+hours"]').click()
    single_page_scrolling()
    web.find_element(By.CSS_SELECTOR, '#field > tbody > tr:nth-child(12) > td.StandardFieldTable_TableCell2 > select').send_keys("Inbound")
    # web.find_element(By.CSS_SELECTOR, '#N1027A').click()
    web.find_element(By.XPATH,
                     '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div[2]/content/form/div[4]/span[1]/a').click()

    # below is using try...except
    # try:
    #     # web.find_element(By.CSS_SELECTOR, '#N104C9').click()
    #     web.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div[2]/content/form/div[4]/span[1]/a').click()
    # except NoSuchElementException:
    #     try:
    #         web.find_element(By.CSS_SELECTOR, '#N1048F').click()
    #     except NoSuchElementException:
    #         web.find_element(By.CSS_SELECTOR, '#N104CC').click()


def check_cisco_12hours_failures():
    web.find_element(By.CSS_SELECTOR, '#senderPartyName').send_keys(from_id)
    web.find_element(By.CSS_SELECTOR, 'form>span:nth-child(4)>a').click()


def cisco_12hours_failures_handle(failure_text):
    failure_text_result = web.find_element(By.XPATH, '//*[@id="queryResults"]/tbody').text.split("\n")
    if failure_text[1] == "The search returned no messages.":
        return f"发送者：{from_id}, 没有进来失败文件."
        # return f"Sender：{from_id}, No incoming failures."
    else:
        return f"发送者：{from_id}, 有{len(failure_text_result[1:])}个文件失败！"
        # return f"Sender：{from_id}, {len(failure_text_result[1:])} failures！"


def check_cisco_inbound():
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
        # return f"More than 100 messages received in 1 hour"
    elif len(inbound_text[1::20]) > 0:
        number = len(inbound_text[1::20])
        return f"一小时内收到进来文件不小于f{4 * number}"
        # return f"Mor than {4 * number} messages received in 1 hour"
    else:
        return f"一小时内没有文件进来！"
        # return f"No messages received in 1 hour！"


def single_page_scrolling():
    js = "window.scrollBy(0,500)"
    js_top = "window.scrollTo(0,-document.body.scrollHeight)"
    for _ in range(2):
        sleep(3)
        web.execute_script(js)
    sleep(3)
    web.execute_script(js_top)


def choose_check_stream():
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
    return url, choice


def send_phone_message(content):
    data = urllib.parse.urlencode({'u': phonemessage_user, 'p': phonemessage_password, 'm': PHONE_NUM, 'c': content})
    send_url = phonemessage_smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print(phonemessage_statusStr[the_page], current_time)


def send_mail(resp_text, subject_choice):
    outlook = win32.Dispatch('Outlook.Application')

    main_item = outlook.CreateItem(0)
    # email address luis.liu is just for testing
    main_item.Recipients.Add('luis.liu@dbschenker.com')
    # main_item.Recipients.Add('support.sword-csd@dbschenker.com')
    # RejectReason = 'Messaging.Transport.RetryFailure.RetriesExhausted'"
    # subject_time = datetime.now().strftime('%H:%M:%S')
    subject_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # main_item.Subject = f"PME_Message Tracker Failure Checking for {steams_dict[f'{subject_choice}']} {subject_time}"
    main_item.Subject = f"PME_{steams_dict[f'{subject_choice}']}_Message Tracker Inbound Failure Checking {subject_time}"

    main_item.BodyFormat = 2
    main_item.HTMLBody = email_main_body(resp_text)
    main_item.Send()


def email_main_body(handle_text):
    header = '''<H3>Dear ITSD Team, kindly assign To:SWORD:AO</H3>'''
    signature = '''    
    <br><br>
    <font size="2", color="#1F4E79">Mit freundlichen Grüßen / Best regards,<br>--<br>
    <font-weight: bold >Luis Liu<br>2nd  Level Support<br>
     GTECH, Global Technology, Architecture and IT Services (F.LCA)<br><br>
    Application Operations & Support<br>Technology Solution Center (L.LCS)<br><br>
    Schenker Shared Services (Nanjing) Co., Ltd.<br>
    Building 7, Jiangsu Software Park, No. 699 -22 Xuanwu Avenue, 210042 Nanjing, P.R. China<br><br>
    Phone: +86 25 6964-1709<br>E-Mail: <a href="luis.liu@dbschenker.com"> luis.liu@dbschenker.com</a>
    URL <a href="www.dbschenker.com"> www.dbschenker.com </a><br>
    Service Desk: +49 201 59 25 25 25<br></font><br>'''
    failure_list = handle_text.split("\n")
    # print(failure_list)
    inbound_ids, outbound_ids = [], []
    if failure_list[1][0:3] != "The":
        inter_element = ""
        failure_list_length = len(failure_list)
        for element in failure_list[1:]:
            if element.split()[0] != "Details" or len(element.split()) <= 10:
                for single_bad_element in element.split():
                    inter_element += single_bad_element + " "
                index = failure_list.index(element)
                del failure_list[index]
        if len(failure_list) != failure_list_length:
            failure_list.append(inter_element)
        for element in failure_list[1:]:
            if "Outbound" in element.split():
                outbound_ids.append(element.split()[9])
            else:
                inbound_ids.append(element.split()[8])
    line2, line4 = '', ''
    line1 = f"<div>There are totally {len(inbound_ids)} inbound failures as below:</div>"
    for inbound in set(inbound_ids):
        line2 += f"<div>{inbound_ids.count(inbound)} failures from_ID: {inbound}.</div>"
    line3 = f"<div>There are totally {len(outbound_ids)} outbound failures as below:</div>"
    for outbound in set(outbound_ids):
        # print(f"{outbound_ids.count(outbound)} failures from_ID: {outbound}.")
        line4 += f"<div>{outbound_ids.count(outbound)} failures To_ID: {outbound}.</div>"
    body = line1 + line2 + line3 + line4

    return f'''{header} <div>General result for failures last 12 hours~~~~</div><H4> {body} </H4>
            <div>Latest failure happened at: {failure_list[1].split()[5:8]}</div><div>Details as be
            low: ~~~~</div>  {handle_text} <div>~~~~</div> {signature}'''


def main(stream_url, stream_choice):
    # create web driver. chrome can't used any longer
    # web=create_chrome_drive()
    # web = create_chrome_drive(headless=True)
    # web = create_firefox_drive()
    global web
    web = create_edge_drive()
    # web = create_firefox_drive()
    web.implicitly_wait(10)

    # log in
    log_in(stream_url)
    # check failures last 12 hours
    sleep(15)
    check_12hours_failures()

    # send out email for failure checking result.
    failure_text = web.find_element(By.XPATH, '//*[@id="queryResults"]/tbody').text

    # below 4 lines: only send out failures if there are inbound failures
    if "Inbound" in failure_text.split(" "):
        send_mail(failure_text, stream_choice)
        print("Checking Complete!")
    else:
        print("No inbound Failures!")

    # send out failure result
    send_mail(failure_text, stream_choice)

    # check Cisco inbound messages last 1 hour. Not use till further notification
    if stream_choice == "x":
        check_cisco_12hours_failures()
        failure_content = cisco_12hours_failures_handle(failure_text)
        try:
            check_cisco_inbound()
        except Exception as value_err:
            print(value_err)
        content = "【luis】" + failure_content + inbound_info_handle() + ": " + current_time
        print(content)
        # send_phone_message(content)

    # web.quit()


if __name__ == '__main__':

    # choose the steam you wan to check
    current_time = datetime.now().strftime('%m-%d %H:%M:%S')
    monitoring_url, monitoring_stream = choose_check_stream()

    main(monitoring_url, monitoring_stream)
    if monitoring_stream == 'v':
        schedule.every().hour.at(":01").do(main, stream_url=monitoring_url, stream_choice=monitoring_stream)
    else:
        # schedule.every().day.at('17:00').do(main, stream_url=monitoring_url, stream_choice=monitoring_stream)
        # schedule.every().day.at('19:00').do(main, stream_url=monitoring_url, stream_choice=monitoring_stream)
        schedule.every().day.at('21:00').do(main, stream_url=monitoring_url, stream_choice=monitoring_stream)
        # schedule.every().day.at('23:00').do(main, stream_url=monitoring_url, stream_choice=monitoring_stream)

    while True:
        schedule.run_pending()
        sleep(1)
