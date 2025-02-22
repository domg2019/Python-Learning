import requests
import warnings
import pyttsx3
from datetime import datetime

from lxml import etree

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
    login_url = "https://b2bisecdep1.sl3-test.comp.db.de/icingaweb2/authentication/login"
    login_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
    }
    payload = {
        "username": "LUISLIU1",
        "password": "LUISLIU1",
    }
    res = requests.get(login_url, verify=False, headers=login_headers, json=payload)
    cookies = res.cookies
    cookie_key_value = requests.utils.dict_from_cookiejar(cookies)['Icingaweb2']
    cookie = "icingaweb2-announcements=%7B%22acknowledged%22%3A%5B%22ef42b5fb05792ac30d436719a3421fb0%22%2C%22d15df29c22146f2f227f3316cb72d4df%22%5D%2C%22etag%22%3Anull%2C%22next%22%3Anull%7D; Icingaweb2=" + cookie_key_value + "; icingaweb2-tzo=28800-0"
    url = 'https://b2bisecdep1.sl3-test.comp.db.de/icingaweb2/monitoring/list/services?service_problem=1&sort=service_severity&dir=desc'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
        # "Cookie": "icingaweb2-announcements=%7B%22acknowledged%22%3A%5B%22ef42b5fb05792ac30d436719a3421fb0%22%2C%22d15df29c22146f2f227f3316cb72d4df%22%5D%2C%22etag%22%3Anull%2C%22next%22%3Anull%7D; Icingaweb2=n64ubl2ilqm9uo49hdn1e2sp3b; icingaweb2-remember-me=H5YuNRMmv1A%3D%7CVa4R4MRwKNkytd1zd5xQ2g%3D%3D%7C3lc%2BLyzGCjC%2BeyAU; icingaweb2-session=1665046753; icingaweb2-tzo=28800-0",
        # "Cookie": "icingaweb2-announcements=%7B%22acknowledged%22%3A%5B%22ef42b5fb05792ac30d436719a3421fb0%22%2C%22d15df29c22146f2f227f3316cb72d4df%22%5D%2C%22etag%22%3Anull%2C%22next%22%3Anull%7D; Icingaweb2=sap0o7ekbffjaociq8svmsf91d; icingaweb2-tzo=28800-0",
        "Cookie": "icingaweb2-announcements=%7B%22acknowledged%22%3A%5B%22ef42b5fb05792ac30d436719a3421fb0%22%2C%22d15df29c22146f2f227f3316cb72d4df%22%5D%2C%22etag%22%3Anull%2C%22next%22%3Anull%7D; Icingaweb2=sap0o7ekbffjaociq8svmsf91d; icingaweb2-tzo=28800-0",
        # "Cookie": cookie,
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
            speak("Congratulation!!!")

check_service_problems()

