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
SNOW_URL = "https://schenkeritsmprod.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_fixed_query%3D%26sysparm_query%3Dactive%253Dtrue%255Eassigned_toISEMPTY%255Eassignment_group%253D72a692a3dbfdb2401529f3571d96191d%255EORassignment_group%253Dcee88b9cdb781344eafffd651d961913%255EORassignment_group%253D8a127011db2a76001529f3571d961956%255EORassignment_group%253D2f3642361b383410ad1499339b4bcb12%255EORassignment_group%253D46b6c9091b2ee8104b6087306b4bcb7b%26sysparm_clear_stack%3Dtrue"
driver = webdriver.Edge()   # Edge
# driver = webdriver.Firefox()   # Firefox
driver.get(SNOW_URL)  # 刷新网址

for i in range(666):  # 刷新次数
    driver.refresh()  # 刷新网页
    sleep(10)  # 10S一次


# driver = webdriver.Firefox()
# # snow_page = SNOW_URL
# driver.get(SNOW_URL) # 刷新网址



# driver_edge = create_edge_drive()  # 需要 下载 对应浏览器 驱动到 python 安装目录
# driver_edge.get("https://schenkeritsmprod.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_fixed_query%3D%26sysparm_query%3Dactive%253Dtrue%255Eassigned_toISEMPTY%255Eassignment_group%253D72a692a3dbfdb2401529f3571d96191d%255EORassignment_group%253Dcee88b9cdb781344eafffd651d961913%255EORassignment_group%253D8a127011db2a76001529f3571d961956%255EORassignment_group%253D2f3642361b383410ad1499339b4bcb12%255EORassignment_group%253D46b6c9091b2ee8104b6087306b4bcb7b%26sysparm_clear_stack%3Dtrue")  # 刷新网址


# for i in range(1000):  # 刷新次数
#     driver_firefox.refresh()  # 刷新网页
#     sleep(600)  # 10分钟一次
#     # driver_edge.refresh()
#     # sleep(600)





'''fail to install PyQt5 module'''
# import sys
#
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
#
#
# class WebView(QWebEngineView):
#     def __init__(self):
#         super(WebView, self).__init__()
#         url = 'https://schenkeritsmprod.service-now.com/now/nav/ui/classic/params/target/incident_list.do%3Fsysparm_fixed_query%3D%26sysparm_query%3Dactive%253Dtrue%255Eassigned_toISEMPTY%255Eassignment_group%253D72a692a3dbfdb2401529f3571d96191d%255EORassignment_group%253Dcee88b9cdb781344eafffd651d961913%255EORassignment_group%253D8a127011db2a76001529f3571d961956%255EORassignment_group%253D2f3642361b383410ad1499339b4bcb12%255EORassignment_group%253D46b6c9091b2ee8104b6087306b4bcb7b%26sysparm_clear_stack%3Dtrue'  # 自定义刷新的网页
#         self.load(QUrl(url))
#         self.showMinimized()  # 窗口最小化
#         self.show()
#         self.thread = Worker()  # 创建线程实例
#         self.thread.sinOut.connect(self.reloadWeb)  # 信号绑定槽函数
#         self.thread.start()  # 开启线程
#
#     def reloadWeb(self):
#         self.reload()  # 刷新网页
#
#
# class Worker(QThread):
#     sinOut = pyqtSignal()  # 创建新的信号，并且有参数
#     num = 0
#
#     def __init__(self, parent=None):  # 构造方法 创建号对象之后，会自动调用
#         super(Worker, self).__init__(parent)
#
#     def __del__(self):  # 析构函数 再对象被删除 和 回收的时候调用
#         self.wait()
#
#     def run(self):
#         for i in range(1000):
#             # 发出信号
#             self.sinOut.emit()  # 给信号传参字符串，并发送
#             # 线程休眠66秒
#             self.sleep(66)
#             Worker.num = Worker.num + 1
#             print(str(Worker.num) + " 次刷新")
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     web = WebView()
#     print('### exec succeed !')
#     sys.exit(app.exec_())
