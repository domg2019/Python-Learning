#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 0:26
# @Author  : Luis Liu
# @Email   : myheartu@126.com
# @File    : web_driver
# @Software: PyCharm


#  -*- coding: utf-8 -*-
#  Author: luis.liu@dbschenker.com
#  Timestamp:  4/11/2023  5:11 PM


from time import sleep
from selenium import webdriver

#config.
SNOW_URL = "https://dbschenker.sharepoint.com/sites/scintilla-/_layouts/15/Doc.aspx?sourcedoc={6ae1e06e-e9f4-4bbb-819d-26276e80fb87}&action=view&wd=target%28Apple.one%7Cf8739b5d-ea5d-450b-b78c-3f8b0f78fe70%2FTesting%7Cb720ce13-708f-4dc4-8289-779fed69edb8%2F%29&wdorigin=NavigationUrl"
driver = webdriver.Edge()   # Edge
# driver = webdriver.Firefox()   # Firefox
driver.get(SNOW_URL)  # 刷新网址

# for i in range(666):  # 刷新次数
#     driver.refresh()  # 刷新网页
#     sleep(10)  # 10S一次

