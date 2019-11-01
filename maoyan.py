#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/31 11:19
# @Author : hhx06
# @Site : 
# @File : maoyan.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import datetime,time
import pymysql
import json

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

    return node

def getList(node):

    tt = node.find("dl", attrs={"class": "movie-list"})
    list = tt.find_all("div", attrs={"class": "movie-item"})
    urls = []
    for li in list:
        href = li.a['href']
        urls.append(href)
    return urls


def getContent(node,maoyan_id):

    banner = node.find('div', attrs={"class": "banner"})
    cover = banner.find('div', attrs={"class": "avatar-shadow"}).img['src']
    name = banner.find('h3', attrs={"class": "name"}).string + '/' + banner.find('div', attrs={"class": "ename"}).string
    ul = banner.find_all('li', attrs={"class": "ellipsis"})
    type = ul[0].string
    date = ul[2].string
    arr = ul[1].string.strip().split('/')
    area = arr[0]
    timelong = arr[1]
    intro = node.find('span', attrs={"class": "dra"}).string
    director = node.find('ul', attrs={"class": "celebrity-list"}).get_text().strip()
    arrs = node.find_all('li', attrs={"class": "actor"})
    actor = ''
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for ar in arrs:
        actor = actor + ar.find('a', attrs={"class": "name"}).get_text().strip() + '/'
    data_us = [maoyan_id, cover, name, type, date, area, timelong, intro, director, actor, dataTime,'1']

    return data_us

def saveToMysql(data):
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    try:
        cur.executemany(
            "insert into mao_yans(maoyan_id,cover,name,type,date,area,timelong,intro,director,actor,created_at,mold) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            data)
        conn.commit()

    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()

def main():
    url = 'https://maoyan.com/films?showType=1'
    node = getHtml(url)
    urls = getList(node)
    url_pre = 'https://maoyan.com'
    data = []
    for url1 in urls:
        maoyan_id = url1.split('/')[2]
        url1 = url_pre + url1
        node1 = getHtml(url1)
        con = getContent(node1,maoyan_id)
        data.append(con)
    saveToMysql(data)
    print('end')
main()