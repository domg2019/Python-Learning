#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 1:05
# @Author  : Luis Liu
# @Email   : myheartu@126.com
# @File    : test_storelog.py
# @Software: PyCharm

from datetime import datetime
subject_time = datetime.now().strftime('%Y-%m-%d')

test = "test for log archive"
test2 = "icinga"

for i in range(3):
    with open(f"./test/icinga_{subject_time}.log", "a") as f:
        f.write(f"{test} {test2}\n")

print(test, subject_time)
