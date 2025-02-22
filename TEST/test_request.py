#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/31 17:36
# @Author  : Luis Liu
# @Email   : myheartu@126.com
# @File    : test_eipaas_runtime
# @Software: PyCharm

import requests


runtime_url = "https://dbschenker.sharepoint.com/:o:/r/sites/scintilla-/_layouts/15/Doc.aspx?sourcedoc=%7B6ae1e06e-e9f4-4bbb-819d-26276e80fb87%7D&action=view&wd=target(Apple.one%7Cf8739b5d-ea5d-450b-b78c-3f8b0f78fe70%2FTesting%7Cb720ce13-708f-4dc4-8289-779fed69edb8%2F)&wdorigin=NavigationUrl"

resp = requests.get(runtime_url)

print(resp.text)