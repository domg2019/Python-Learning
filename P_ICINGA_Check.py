import requests
import warnings
import re
import pyttsx3
from time import sleep
from datetime import datetime

from lxml import etree
import schedule


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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
        "Cookie": "icingaweb2-session=1660751557; Icingaweb2=oajl1pl6e99lk493fr7ua73303; icingaweb2-announcements=%7B%22acknowledged%22%3A%5B%22ef42b5fb05792ac30d436719a3421fb0%22%5D%2C%22etag%22%3A%22aebb562b%22%2C%22next%22%3A%221660728225%22%7D; icingaweb2-tzo=28800-0",

    }
    warnings.filterwarnings("ignore")
    resp = requests.get(url, verify=False, headers=headers)
    html = etree.HTML(resp.text)
    segments_list = html.xpath('/html/body//table/tbody/tr')
    current_time = datetime.now().strftime('%m-%d %H:%M:%S')

    # Detect if request is successful
    if len(segments_list) != 0:
        print("Request Successful!" + current_time)

    # handle resp results
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
                        if int(re.search(r'([0-9]+)m', elements_list[1]).group(1)) >= 5:
                            print("New alert more than 5 minutes! See details below: ")
                            speak("Attention Attention Attention! New alert more than 5 minutes! See details below: ")
                            for element in elements_list:
                                print(element.strip("\n").strip(" "))
                else:
                    critical_time = elements_list[1].strip("\n").strip(" ")
                    print(f"check if there is a ticket. One critical alert is existed {critical_time}")


# schedule job setup
schedule.every(5).minutes.until('23:10').do(check_service_problems)

while True:
    schedule.run_pending()
    sleep(1)
