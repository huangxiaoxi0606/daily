#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/1 16:57
# @Author : hhx06
# @Site : 
# @File : Lasa.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://you.ctrip.com/travels/lhasa36/t3-p2.html'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-Language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    response = requests.get(url, headers=headers)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')
    list = soup.find_all("a", attrs={"class": "journal-item"})
    # 遍历存储即可
    for li in list:
        print(li)
        exit(0)
        
main()
