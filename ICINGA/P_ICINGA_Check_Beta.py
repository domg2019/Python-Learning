import requests
import warnings
import re
import pyttsx3
from datetime import datetime
from time import sleep

from lxml import etree
import schedule

CRITICAL_ALERTS_COUNT = 8


def speak(audio):
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    new_voice_rate = 130
    engine.setProperty('rate', new_voice_rate)
    engine.setProperty('voice', voice[1].id)
    engine.say(audio)
    engine.runAndWait()


def check_service_problems():
    url = 'https://b2biprddep1.sl3.comp.db.de/icingaweb2/monitoring/list/services?service_problem=1&sort=service_severity&dir=desc'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
        "Cookie": "Icingaweb2=55v2vgsolqr01jo6llu8sbkq4p; icingaweb2-remember-me=a53JIpxMOVg%3D%7CTnxTZVRyXi3OEb3%2Bi1j74w%3D%3D%7C94eKBWIYP8LwCODa; icingaweb2-session=1724571151; icingaweb2-tzo=28800-0",
    }
    warnings.filterwarnings("ignore")
    try:
        resp = requests.get(url, verify=False, headers=headers)
    except Exception as error_value:
        print(error_value)
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
            # handle resp results

            critical_list = []
            for segment in segments_list:
                if segment.xpath('.//span/i/@aria-label')[0] == 'Unhandled':
                    general_elements_list = segment.xpath('.//text()')
                    # print(general_elements_list)
                    elements_list = [general_element for general_element in general_elements_list
                                     if general_element.strip("\n").strip(" ") != ""]
                    if elements_list[0].strip("\n").strip(" ") == "CRITICAL":
                        critical_list.append(elements_list[0].strip("\n").strip(" "))
            if len(critical_list) >= CRITICAL_ALERTS_COUNT:
                speak(f"Attention Attention Attention!{len(critical_list)} unhandled critical alerts")
                print(f"{len(critical_list)} unhandled critical alerts")
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
                            #
                            # dictionary for regular failures less than 30 minutes
                            #
                            regular_failure_dict = ["Custom meta load", ]
                            print(elements_list)
                            if elements_list[2].strip("\n").strip(" ")[0:16] in regular_failure_dict:
                                print("test")
                                if re.search(r'[0-9]([a-z])', elements_list[1]).group(1) == "m":
                                    if 30 <= int(re.search(r'([0-9]+)m', elements_list[1]).group(1)) <= 33:
                                        print("New alert more than 5 minutes! See details below: ")
                                        speak("Attention! New alert!")
                                        speak(elements_list[1].strip("\n").strip(" "))
                                        speak(elements_list[2].strip("\n").strip(" ")[0:16])
                                        for element in elements_list:
                                            print(element.strip("\n").strip(" "))
                            elif elements_list[1][0:3] == "for":
                                if re.search(r'[0-9]([a-z])', elements_list[1]).group(1) == "m":
                                    # print(re.search(r'[0-9]([a-z])', elements_list[1]).group(1))
                                    if 3 <= int(re.search(r'([0-9]+)m', elements_list[1]).group(1)) <= 6:
                                        print("New alert more than 5 minutes! See details below: ")
                                        speak("Attention! New alert!")
                                        speak(elements_list[1].strip("\n").strip(" "))
                                        speak(elements_list[2].strip("\n").strip(" ")[0:16])
                                        for element in elements_list:
                                            print(element.strip("\n").strip(" "))
                            else:
                                critical_time = elements_list[1].strip("\n").strip(" ")
                                print(f"check if there is a ticket. One critical alert is existed {critical_time}")


check_service_problems()
# schedule job setup
schedule.every(3).minutes.until('23:05').do(check_service_problems)

while True:
    schedule.run_pending()
    sleep(1)
