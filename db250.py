#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/23 15:45
# @Author : hhx06
# @Site : 
# @File : db250.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
def main():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'Host': 'www.228.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    url = 'https://movie.douban.com/top250?start=0&filter='
    response = requests.get(url,headers=headers)
    node = BeautifulSoup(response.text, 'html.parser')
    lists = node.find('ol')
    list = lists.find_all('li')
    data = []
    for li in list:
        # data['img'] = li.img['src']
        # data['no'] = li.em.string
        s1 = li("span",attrs={"class":"title"})
        s = s1.get_text()
        print(s)
        exit(0)



main()