#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/8 8:53
# @Author : hhx06
# @Site : 
# @File : db_music.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import pymysql
import datetime,time
def getHtml(url):
    """
    解析页面html
    :param url:
    :return:
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',

        'Connection': 'keep-alive',
        'Host': 'music.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    response = requests.get(url, headers=headers)
    node = BeautifulSoup(response.text, 'html.parser')
    return node

def parseList(node,no):
    """
    解析列表页面
    :param node:
    :return:
    """
    items =node.find_all("tr", attrs={"class": "item"})
    data = []
    urls = []
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for item in items:
        no = int(no) + 1
        href = item.a['href']
        img = item.img['src']
        div = item.find("div", attrs={"class": "pl2"})
        title = div.a.get_text().replace("\n", "").replace(" ", "")
        intro = div.find("p", attrs={"class": "pl"}).string
        h = intro.split('/')
        type = cd = album = date = sing_name =''
        if(len(h)>4):
            type = h[4]
        if (len(h) > 3):
            cd = h[3]
        if (len(h) > 2):
            album = h[2]
        if (len(h) > 1):
            date = h[1]
        if(len(h)>0):
            sing_name = h[0]
        star = item.find("span", attrs={"class": "rating_nums"}).string
        comment = item.find("span", attrs={"class": "pl"}).string.replace("\n", "").replace(" ", "")
        data.append([no,img,title,sing_name,date,album,cd,type,star,comment,dataTime])
        urls.append([no,href])
    return data,urls



def listToMysql(data):
    """
    列表数据存入数据库
    :param data:
    """
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    try:
        cur.executemany(
            "insert into db_music_tops(no,img,title,sing_name,date,album,cd,type,star,comment,created_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            data)
        conn.commit()
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()

def parseUrl(urls):
    """
    解析页面url
    :param urls:
    """
    for url in urls:
        nodes = getHtml(url[1])
        no = url[0]
        parseContent(nodes,no)

def parseContent(nodes,no):
    """
    页面数据存入数据库
    :param nodes:
    """
    intro = nodes.find("span", attrs={"property": "v:summary"})
    if (intro):
        intro = intro.get_text().strip()
    else:
        intro = ""
    songs = nodes.find("div", attrs={"class": "track-list"}).get_text().strip()
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    try:
        cur.execute(
            "update db_music_tops set intro = %s,songs = %s,updated_at = %s  where no =%s",
            (intro, songs, dataTime, no))
        conn.commit()
    except Exception as err:
        print(err)
        exit(0)
    finally:
        cur.close()
        conn.close()

def main():
    """
    主程序
    """
    hh = ['0', '25', '50', '75', '100', '125', '150', '175', '200', '225']

    for h in hh:
        url = 'https://music.douban.com/top250?start='+h+''
        node = getHtml(url)
        data,urls = parseList(node,h)
        listToMysql(data)
        parseUrl(urls)


    print('end')
    exit(0)
main()