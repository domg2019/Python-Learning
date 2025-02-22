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

def speak(audio):
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 130)
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(audio)
    engine.runAndWait()


def send_mail(alert_count):
    outlook = win32.Dispatch('Outlook.Application')
    main_item = outlook.CreateItem(0)
    main_item.Recipients.Add('support.sword-csd@dbschenker.com')
    subject_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    main_item.Subject = f"PME_ICINGA_There are more than {alert_count} critical alerts {subject_time}"
    main_item.BodyFormat = 2
    main_item.HTMLBody = email_main_body(f"No less than {alert_count} unhandled alerts on ICINGA")
    main_item.Send()


def email_main_body(handle_text):
    header = "<H3>Dear ITSD Team, kindly assign To:SWORD:AO</H3>"
    signature = """    
    <br><br>
    <font size="2", color="#1F4E79">Mit freundlichen Grüßen / Best regards,<br>--<br>
    Luis Liu<br>2nd Level Support<br>
    GTECH, Global Technology, Architecture and IT Services (F.LCA)<br>
    Schenker Shared Services (Nanjing) Co., Ltd.<br>
    Phone: +86 25 6964-1709<br>
    E-Mail: <a href="luis.liu@dbschenker.com"> luis.liu@dbschenker.com</a>
    </font><br>"""
    return f"{header} <div>Details as below:</div><div>~~~~</div> {handle_text} <div>~~~~</div> {signature}"


def login():
    """Logs in and returns session cookies."""
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
    }
    response = session.post(LOGIN_URL, data=data, headers=headers, verify=False)
    if response.status_code == 200:
        print("Login successful.")
    else:
        print("Login failed.")
        speak("Attention! Login failed!")

def get_latest_cookie():
    """Retrieve and return the latest cookies after login."""
    login()  # Ensure login is performed first
    return session.cookies.get_dict()  # Return the session's latest cookies

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

    print(f"Request Successful! {datetime.now().strftime('%m-%d %H:%M:%S')}")

    segments_list = html.xpath('/html/body//table/tbody/tr')
    critical_list = []

    for segment in segments_list:
        if segment.xpath('.//span/i/@aria-label')[0] == 'Unhandled':
            elements_list = [text.strip() for text in segment.xpath('.//text()') if text.strip()]
            if elements_list and elements_list[0] == "CRITICAL":
                critical_list.append(elements_list[0])

    if len(critical_list) >= CRITICAL_ALERTS_COUNT:
        speak(f"Attention! {len(critical_list)} unhandled critical alerts")
        send_mail(len(critical_list))
        speak("General email sent to ITSD! Please check.")
    else:
        for segment in segments_list:
            if segment.xpath('.//span/i/@aria-label')[0] == 'Unhandled':
                elements_list = [text.strip() for text in segment.xpath('.//text()') if text.strip()]
                if elements_list and elements_list[0] == "CRITICAL":
                    alert_time = elements_list[1]
                    if "for" in alert_time and re.search(r'(\d+)m', alert_time):
                        alert_minutes = int(re.search(r'(\d+)m', alert_time).group(1))
                        if 3 <= alert_minutes <= 6 and elements_list[2][:16] not in IGNORE_DICT:
                            speak("Attention! New alert!")
                            print(f"New alert: {alert_time} - {elements_list[2][:16]}")


# Login and schedule the job
login()
schedule.every(3).minutes.until('23:25').do(check_service_problems)

while True:
    schedule.run_pending()
    sleep(1)
