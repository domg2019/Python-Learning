import time
from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from time import sleep
from datetime import datetime
import urllib.request

from win32com import client as win32
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from settings import *


opt = webdriver.FirefoxOptions()
# opt.add_argument("--headless")
# opt.add_argument('--disable-gpu')
# opt.add_argument("useAutomationExtension", False)
# opt.add_argument('excludeSwitches', ['enable-automation'])
# opt.add_argument('detach', True)
firefox_binary = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
executable_path = "C:\\Users\LUISLIU1\\Desktop\\python\\geckodriver-v0.31.0-win64\\geckodriver.exe"

web = webdriver.Firefox(firefox_binary=firefox_binary, executable_path=executable_path)

url="https://b2bi8-sword.dc.signintra.com/ui/"
web.implicitly_wait(10)

def log_in(url):
    web.get(url)
    web.maximize_window()
    web.find_element(By.CSS_SELECTOR,'#loginUserId').clear()
    web.find_element(By.CSS_SELECTOR,'#loginUserId').send_keys(user_id)
    web.find_element(By.CSS_SELECTOR,'#loginPassword').clear()
    web.find_element(By.CSS_SELECTOR,'#loginPassword').send_keys(password,Keys.ENTER)

log_in(url)
time.sleep(1)
# web.find_element(By.CSS_SELECTOR, '#advancedButton').click()
# web.find_element(By.CSS_SELECTOR, '#advancedButton').click()
# web.find_element(By.CSS_SELECTOR, '#exceptionDialogButton').click()
#advancedButton