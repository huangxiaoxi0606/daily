#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/8 10:36
# @Author : hhx06
# @Site : 
# @File : music.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup

def main():

    url = 'https://music.douban.com/subject/1788174/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',

        'Connection': 'keep-alive',
        'Host': 'music.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    response = requests.get(url, headers=headers)
    node = BeautifulSoup(response.text, 'html.parser')
    songs = node.find("div", attrs={"class": "track-list"}).get_text().strip()
    print(songs)
    exit(0)



main()