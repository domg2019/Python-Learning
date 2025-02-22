import requests
import warnings
import re
import pyttsx3
from datetime import datetime
from time import sleep
from lxml import etree
from win32com import client as win32
import schedule

# Suppress only InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

CRITICAL_ALERTS_COUNT = 10
IGNORE_DICT = ['Custom meta load']
DATE = datetime.now().strftime('%Y-%m-%d')

LOGIN_URL = "https://b2biprddep1.sl3.comp.db.de/icingaweb2/authentication/login"
DASHBOARD_URL = "https://b2biprddep1.sl3.comp.db.de/icingaweb2/monitoring/list/services?service_problem=1&sort=service_severity&dir=desc"

USERNAME = "LUISLIU1"
PASSWORD = "LUISLIU1"

session = requests.Session()

def check_service_problems():
    cookies = get_latest_cookie()  # Automatically get the latest cookie
    if not cookies:
        speak("Attention! Login failed! Check your credentials!")
        return

    url = ('https://b2biprddep1.sl3.comp.db.de/icingaweb2/monitoring/list/services?service_problem=1&sort=service'
           '_severity&dir=desc')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
    }

    session = requests.Session()
    session.cookies.update(cookies)  # Apply latest cookie

    warnings.filterwarnings("ignore")
    try:
        resp = session.get(url, headers=headers, verify=False)
    except Exception as error_value:
        print(error_value)
        speak("Warning! Warning! Connection issue!")
        return

    html = etree.HTML(resp.text)

    # Detect if login failed
    is_login = html.xpath('/html/body/div[1]/div[1]/@id')  # Fetch div-id: login
    if is_login and is_login[0] == "login":
        speak("Attention! Login failed! Retrying...")
        check_service_problems()  # Retry login
    else:
        print("✅ Successfully logged in and retrieved dashboard data.")
        # Continue your normal process...

check_service_problems
