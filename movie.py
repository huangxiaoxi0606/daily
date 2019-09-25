#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/25 9:40
# @Author : hhx06
# @Site : 
# @File : movie.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup

def getHtml(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    node = BeautifulSoup(response.text, 'html.parser')
    return node

def parseList(node):
    data = []
    hh = node.find(id="content")
    no = hh.find("span", attrs={"class": "top250-no"}).string[3:]
    print(no)
    exit(0)
    # data['year'] = hh.find("span", attrs={"class": "year"}).string
    s1 = hh.find(id = "info")
    # s2 = s1.find_all("span", attrs={"class": "attrs"})
    # data['director'] = s2[0].string
    # data['screen_writer'] = s2[1].get_text()
    # data['actor'] = s2[2].get_text()
    # s3 = s1.find_all("span", attrs={"property":"v:genre"})
    # s4 = ''
    # for s in s3:
    #     s4 = s4 + s.string + '/'
    # data['type'] = s4
    # data['time_long'] = s1.find("span", attrs={"property":"v:runtime"}).string
    # s5 = s1.find_all("span", attrs={"property": "v:initialReleaseDate"})
    # s6 = ''
    # for h in s5:
    #     s6 = s6 + h.string + '/'
    # data['release_date'] = s6
    # data['intro'] = hh.find("span", attrs={"property": "v:summary"}).strip()


    exit(0)

def main():
    url = 'https://movie.douban.com/subject/1307914/'
    node = getHtml(url)

    parseList(node)



main()