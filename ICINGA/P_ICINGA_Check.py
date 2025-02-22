import requests
import warnings
import re
import pyttsx3
from datetime import datetime
from time import sleep

from lxml import etree
from win32com import client as win32
import schedule

CRITICAL_ALERTS_COUNT = 10
# CRITICAL_ALERTS_COUNT = 0
IGNORE_DICT = ['Custom meta load']
DATE = datetime.now().strftime('%Y-%m-%d')

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    new_voice_rate = 130
    engine.setProperty('rate', new_voice_rate)
    engine.setProperty('voice', voice[1].id)
    engine.say(audio)
    engine.runAndWait()


def send_mail(alert_count):
    outlook = win32.Dispatch('Outlook.Application')

    main_item = outlook.CreateItem(0)
    # main_item.Recipients.Add('luis.liu@dbschenker.com')
    main_item.Recipients.Add('support.sword-csd@dbschenker.com')
    # RejectReason = 'Messaging.Transport.RetryFailure.RetriesExhausted'"
    # subject_time = datetime.now().strftime('%H:%M:%S')
    subject_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # main_item.Subject = f"PME_Message Tracker Failure Checking for {steams_dict[f'{subject_choice}']} {subject_time}"
    main_item.Subject = f"PME_ICINGA_There are more than {f'{alert_count}'} critical alerts {subject_time}"

    main_item.BodyFormat = 2
    main_item.HTMLBody = email_main_body(f"No less than {alert_count} unhandled alerts on ICINGA")
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
    # failure_list = handle_text.split("\n")
    # # print(failure_list)
    # inbound_ids, outbound_ids = [], []
    # if failure_list[1][0:3] != "The":
    #     inter_element = ""
    #     failure_list_length = len(failure_list)
    #     for element in failure_list[1:]:
    #         if element.split()[0] != "Details" or len(element.split()) <= 10:
    #             for single_bad_element in element.split():
    #                 inter_element += single_bad_element + " "
    #             index = failure_list.index(element)
    #             del failure_list[index]
    #     if len(failure_list) != failure_list_length:
    #         failure_list.append(inter_element)
    #     for element in failure_list[1:]:
    #         if "Outbound" in element.split():
    #             outbound_ids.append(element.split()[9])
    #         else:
    #             inbound_ids.append(element.split()[8])
    # line2, line4 = '', ''
    # line1 = f"<div>There are totally {len(inbound_ids)} inbound failures as below:</div>"
    # for inbound in set(inbound_ids):
    #     line2 += f"<div>{inbound_ids.count(inbound)} failures from_ID: {inbound}.</div>"
    # line3 = f"<div>There are totally {len(outbound_ids)} outbound failures as below:</div>"
    # for outbound in set(outbound_ids):
    #     # print(f"{outbound_ids.count(outbound)} failures from_ID: {outbound}.")
    #     line4 += f"<div>{outbound_ids.count(outbound)} failures To_ID: {outbound}.</div>"
    # body = line1 + line2 + line3 + line4

    return f'''{header} <div>Details as below: </div><div>~~~~</div>  {handle_text} <div>~~~~</div> {signature}'''


def check_service_problems(icinga_cookie):
    url = ('https://b2biprddep1.sl3.comp.db.de/icingaweb2/monitoring/list/services?service_problem=1&sort=service'
           '_severity&dir=desc')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
        # "Cookie": "Icingaweb2=ig0icv30joag79lcuhbnafu29i; icingaweb2-remember-me=UqHua90qY10%3D%7CTG7UQ5O2mi%2B3nsUwDGXzXw%3D%3D%7Cz7nMcMrOej8Xc5GR; icingaweb2-tzo=28800-0; icingaweb2-session=1725867164",
        "Cookie": icinga_cookie,
    }
    warnings.filterwarnings("ignore")
    try:
        resp = requests.get(url, verify=False, headers=headers)
    except Exception as error_value:
        print(error_value)
        with open(f"./log/icinga_{DATE}.log", "a") as f:
            f.write(f"{error_value}\n")
        speak("Warning! Warning! Warning!")
    else:
        html = etree.HTML(resp.text)
        segments_list = html.xpath('/html/body//table/tbody/tr')
        current_time = datetime.now().strftime('%m-%d %H:%M:%S')

        # check if it's successfully get dashboard page
        is_login = html.xpath('/html/body/div[1]/div[1]/@id')  # fetch div-id: login
        if is_login[0] == "login":
            speak("Attention Attention Attention! login failed!")
        # check the services problem dashboard once login successfully
        else:
            # print general request log
            print("Request Successful!" + current_time)
            with open(f"./log/icinga_{DATE}.log", "a") as f:
                f.write(f"Request Successful!{current_time}\n")
            # handle resp results
            critical_list = []
            for segment in segments_list:
                # if segment.xpath('.//span/i/@aria-label') == '':
                #     print("it's empty")
                if segment.xpath('.//span/i/@aria-label')[0] == 'Unhandled':
                    general_elements_list = segment.xpath('.//text()')
                    # print(general_elements_list)
                    elements_list = [general_element for general_element in general_elements_list
                                     if general_element.strip("\n").strip(" ") != ""]
                    if elements_list[0].strip("\n").strip(" ") == "CRITICAL":
                        critical_list.append(elements_list[0].strip("\n").strip(" "))
            if len(critical_list) >= CRITICAL_ALERTS_COUNT:
                speak(f"Attention Attention Attention!{len(critical_list)} unhandled critical alerts")
# Below function is sending alert email when the number of alerts beyond the limited number;
                send_mail(len(critical_list))
                speak("General email sent to ITSD! Please check!!")
                print(f"{len(critical_list)} unhandled critical alerts")
                with open(f"./log/icinga_{DATE}.log", "a") as f:
                    f.write(f"{len(critical_list)} unhandled critical alerts\n")
            else:
                for segment in segments_list:
                    if segment.xpath('.//span/i/@aria-label')[0] == 'Unhandled':
                        general_elements_list = segment.xpath('.//text()')
                        # print(general_elements_list)
                        elements_list = []
                        for general_element in general_elements_list:
                            if general_element.strip("\n").strip(" ") != "":
                                elements_list.append(general_element)
                        # print(elements_list)
                        if elements_list[0].strip("\n").strip(" ") == 'CRITICAL':
                            if elements_list[1][0:3] == "for":
                                if re.search(r'[0-9]([a-z])', elements_list[1]).group(1) == "m":
                                    if 3 <= int(re.search(r'([0-9]+)m', elements_list[1]).group(1)) <= 6 and elements_list[2].strip("\n").strip(" ")[0:16] not in IGNORE_DICT:
                                    # if 3 <= int(re.search(r'([0-9]+)m', elements_list[1]).group(1)) <= 6:
                                        print("New alert more than 5 minutes! See details below: ")
                                        speak("Attention! New alert!")
                                        speak(elements_list[1].strip("\n").strip(" "))
                                        speak(elements_list[2].strip("\n").strip(" ")[0:16])
                                        with open(f"./log/icinga_{DATE}.log", "a") as f:
                                            f.write(f"New alert more than 5 minutes! See details below: \n")
                                        for element in elements_list:
                                            element_print = element.strip("\n").strip(" ")
                                            print(element_print)
                                            with open(f"./log/icinga_{DATE}.log", "a") as f:
                                                f.write(f"{element_print}\n")
                            else:
                                critical_time = elements_list[1].strip("\n").strip(" ")
                                print(f"check if there is a ticket. One critical alert is existed {critical_time}")
                                with open(f"./log/icinga_{DATE}.log", "a") as f:
                                    f.write(f"check if there is a ticket. One critical alert is existed {critical_time}\n")


print("Kindly input the ICINGA Cookie:")
ICINGA_COOKIE = input()
check_service_problems(ICINGA_COOKIE)
# schedule job setup
# schedule.every(3).minutes.until('23:05').do(check_service_problems)
# schedule.every(1).minutes.do(check_service_problems, ICINGA_COOKIE)
# schedule.every(3).minutes.do(check_service_problems, ICINGA_COOKIE)
schedule.every(3).minutes.until('23:25').do(check_service_problems, ICINGA_COOKIE)

while True:
    schedule.run_pending()
    sleep(1)
