import requests
import warnings
import re
import pyttsx3
from datetime import datetime
from time import sleep

from lxml import etree
import schedule

CRITICAL_ALERTS_COUNT = 8

# speck function
def speak(audio):
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    new_voice_rate = 130
    engine.setProperty('rate', new_voice_rate)
    engine.setProperty('voice', voice[1].id)
    engine.say(audio)
    engine.runAndWait()


def check_service_problems():
    url = 'https://b2bisecdep1.sl3-test.comp.db.de/icingaweb2/monitoring/list/services?service_problem=1&sort=service_severity&dir=desc'
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Cookie": "icingaweb2-application-state=%7B%22acknowledged-messages%22%3A%5B%229abd846a5b2824577f1646e08bd4df9fe69f46d0%22%5D%7D; Icingaweb2=q675r75qq9pe946q5c2pp7ja74; icingaweb2-remember-me=9JKrNKU7DXU%3D%7C1pdwKEWgvBcJcZwNCWyLRA%3D%3D%7CSFq1yRR3yFmIDXVo; icingaweb2-session=1739518619; icingaweb2-tzo=28800-0",
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
                speak(f"Attention Attention Attention! TEST new alert! {len(critical_list)} unhandled critical alerts")
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
                            if elements_list[1][0:3] == "for":
                                if re.search(r'[0-9]([a-z])', elements_list[1]).group(1) == "m":
                                    if 5 <= int(re.search(r'([0-9]+)m', elements_list[1]).group(1)) <= 10:
                                        print("New alert more than 5 minutes! See details below: ")
                                        speak("Attention! TEST new alert!")
                                        speak(elements_list[1].strip("\n").strip(" "))
                                        speak(elements_list[2].strip("\n").strip(" ")[0:16])
                                        for element in elements_list:
                                            print(element.strip("\n").strip(" "))
                            else:
                                critical_time = elements_list[1].strip("\n").strip(" ")
                                print(f"check if there is a ticket. One critical alert is existed {critical_time}")


check_service_problems()
# schedule job setup
schedule.every(5).minutes.until('23:25').do(check_service_problems)

while True:
    schedule.run_pending()
    sleep(1)

