#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 0:53
# @Author  : Luis Liu
# @Email   : myheartu@126.com
# @File    : web_auto_refresth_v2
# @Software: PyCharm

from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options

'''---------------------------configrator----------------------------------------'''
# SNOW_URL = ("https://schenkeritsmprod.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_fixe"
#             "d_query%3D%26sysparm_query%3Dactive%253Dtrue%255Eassigned_toISEMPTY%255Eassignment_group%253D72a692a3db"
#             "fdb2401529f3571d96191d%255EORassignment_group%253Dcee88b9cdb781344eafffd651d961913%255EORassignment_grou"
#             "p%253D8a127011db2a76001529f3571d961956%255EORassignment_group%253D2f3642361b383410ad1499339b4bcb12%255EO"
#             "Rassignment_group%253D46b6c9091b2ee8104b6087306b4bcb7b%26sysparm_clear_stack%3Dtrue")

#   add the new HOF - Intergration AO group
SNOW_URL = ("https://schenkeritsmprod.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_query%3Dactive%253Dtrue%255Eassigned_toISEMPTY%255Eassignment_group%253D72a692a3dbfdb2401529f3571d96191d%255EORassignment_group%253Dcee88b9cdb781344eafffd651d961913%255EORassignment_group%253D8a127011db2a76001529f3571d961956%255EORassignment_group%253D2f3642361b383410ad1499339b4bcb12%255EORassignment_group%253D46b6c9091b2ee8104b6087306b4bcb7b%255EORassignment_group%253D7a76a5ae973939109d623a371153afe3%26sysparm_first_row%3D1%26sysparm_view%3D")
# SNOW_URL = ("https://schenkeritsmprod.service-now.com/now/nav/ui/classic/params/target/home.do")
# SNOW_URL = ("https://www.baidu.com")

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')


driver = webdriver.Edge(options=options)
driver.get(SNOW_URL)    # 刷新网址

for i in range(666):  # 刷新次数
    driver.refresh()  # 刷新网页
    sleep(600)  # 10分钟一次

