#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/17 14:46
# @Author : hhx06
# @Site : 
# @File : history.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import datetime,time
import redis
import csv

re = redis.Redis(host = '127.0.0.1', port = 6379,db = 6, password='')
url = 'http://www.tianqihoubao.com/lishi/zhengzhou/month/'

def getHtml(url):
    response = requests.get(url)
    node = BeautifulSoup(response.text, 'html.parser')
    return node

def parseHtml(node):
    datas = []
    tr_list = node.find_all("tr")
    for data in tr_list[1:]:
        sub_data = data.text.split()
        dates = sub_data[0]
        conditions = sub_data[1:3]
        temperatures = sub_data[3:6]
        datas.append([dates,conditions,temperatures])
    return datas


def main():
    # 201901.html
    data = ['201901', '201902', '201903', '201904', '201905', '201906', '201907', '201908', '201909']
    for d in data:
        d_url = url + d + '.html'
        node = getHtml(d_url)
        datas = parseHtml(node)
    with open('weather.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['date', 'conditions', 'temperatures'])
        writer.writerows(datas)
    print('end')
main()