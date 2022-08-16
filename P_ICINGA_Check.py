import requests
import warnings
import re

from lxml import etree

url = 'https://b2biprddep1.sl3.comp.db.de/icingaweb2/monitoring/list/services?service_problem=1&sort=service_severity&dir=desc'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
    "Cookie": "icingaweb2-session=1660490344; Icingaweb2=g3u9k2jbt4mtvv5ndminohp185; icingaweb2-announcements=%7B%22acknowledged%22%3A%5B%22ef42b5fb05792ac30d436719a3421fb0%22%5D%2C%22etag%22%3A%2247686642%22%2C%22next%22%3A%221659857381%22%7D; icingaweb2-tzo=28800-0",
}

warnings.filterwarnings("ignore")
resp = requests.get(url, verify=False, headers=headers)
# print(resp.text)
html = etree.HTML(resp.text)

# segments_list = html.xpath('/html/body/div[1]/div[3]/div[1]/div[3]/table/tbody/tr')
segments_list = html.xpath('/html/body//table/tbody/tr')
# print(segments_list)
for segment in segments_list:
    general_elements_list = segment.xpath('.//text()')
    # print(general_elements_list)
    elements_list = []
    for general_element in general_elements_list:
        if general_element.strip("\n").strip(" ") != "":
            elements_list.append(general_element)
    if elements_list[0].strip("\n").strip(" ") == 'CRITICAL':
        if elements_list[1][0:3] == "for":
            print(elements_list[1])
            if re.search(r'[0-9]([a-z])', elements_list[1]).group(1) == "m":
                if int(re.search(r'([0-9]+)m', elements_list[1]).group(1)) >= 10:
                    print("New alert more than 10 minutes! See details below: ")
                    for element in elements_list:
                        print(element.strip("\n").strip(" "))
        else:
            critical_time = elements_list[1].strip("\n").strip(" ")
            print(f"check if there is a ticket. One critical alert is existed {critical_time}")


