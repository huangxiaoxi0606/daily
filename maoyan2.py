#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/29 15:37
# @Author : hhx06
# @Site : 
# @File : maoyan.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import pickle

def getHtml(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'Host': 'maoyan.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    node = BeautifulSoup(response.text, 'html.parser')
    return  node


def parseList(node):
    node1 = node.find('dl')
    node2 = node1.find_all('div', attrs={"class": "movie-item"})
    urls =[]
    for n in node2:
        href = n.a['href']
        urls.append(href)


    return urls

def parseContent(nodes):
    tt = nodes.find("div", attrs={"class": "avatar-shadow"})
    img= tt.img['src']
    name = nodes.find("h3", attrs={"class": "name"}).string
    w_name = nodes.find("div", attrs={"class": "ename"}).string
    w = nodes.find_all("li", attrs={"class": "ellipsis"})
    type = w[0].string
    time_long = w[1].string
    release = w[2].string
    intro = nodes.find("span", attrs={"class": "dra"}).string
    ww = nodes.find_all("div", attrs={"class": "celebrity-group"})
    r = ww[0].find_all("div", attrs={"class": "info"})
    d = nodes.find_all("ul",attrs={"class":"celebrity-list"})
    celebrity = d[0].get_text()
    actor = d[1].get_text()
    uu = nodes.find_all("li", attrs={"class": "comment-container"})
    comment =[]
    for u in uu:
        comment.append(u.find("div", attrs={"class": "comment-content"}).string)

    print(img,name,w_name,type,time_long,release,intro,celebrity,actor)
    exit(0)


def main():
    url = 'https://maoyan.com/films'
    node = getHtml(url)
    urls = parseList(node)
    data = []
    for u in urls:
        u1 = 'https://maoyan.com'+u
        nodes = getHtml(u1)



main()