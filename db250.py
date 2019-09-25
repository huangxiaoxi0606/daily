#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/23 15:45
# @Author : hhx06
# @Site : 
# @File : db250.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import pymysql
import datetime,time

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
    lists = node.find('ol')
    list = lists.find_all('li')
    urls = []
    data_us =[]
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for li in list:
        img = li.img['src']
        no = li.em.string
        s1 = li.find_all("span", attrs={"class": "title"})
        c_title = s1[0].string
        if len(s1)>1:
            w_title = s1[1].string.strip()
        else:
            w_title = ""
        rating_num = li("span", attrs={"class": "rating_num"})[0].string
        inq = li("span", attrs={"class": "inq"})[0].string
        comment_num = li("span", attrs={"class": ""})[1].string
        href = li.a['href']
        created_at = dataTime
        data_us.append([img,no,c_title,w_title,rating_num,inq,comment_num,href,created_at])
        urls.append(href)
    return data_us,urls

def listToMysql(data):
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    try:
        cur.executemany(
            "insert into db_tops(img,no,c_title,w_title,rating_num,inq,comment_num,url,created_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            data)
        conn.commit()
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()

def parseUrl(urls):
    for url in urls:
        nodes = getHtml(url)
        parseContent(nodes)


def parseContent(nodes):
    hh = nodes.find(id="content")
    year = hh.find("span", attrs={"class": "year"}).string
    s1 = hh.find(id="info")
    s2 = s1.find_all("span", attrs={"class": "attrs"})
    director = s2[0].get_text()
    if len(s2)>2:
        actor = s2[2].get_text()
        screen_writer = s2[1].get_text()
    elif len(s2) >1:
        actor = ''
        screen_writer = s2[1].get_text()
    else:
        screen_writer = ''
        actor = ''

    s3 = s1.find_all("span", attrs={"property":"v:genre"})
    s4 = ''
    for s in s3:
        s4 = s4 + s.string + '/'
    type = s4
    time_long = s1.find("span", attrs={"property":"v:runtime"}).string
    s5 = s1.find_all("span", attrs={"property": "v:initialReleaseDate"})
    s6 = ''
    for h in s5:
        s6 = s6 + h.string + '/'
    release_date = s6
    intro = hh.find("span", attrs={"property": "v:summary"})
    if(intro):
        intro = intro.get_text().strip()
    else:
        intro =""
    no = hh.find("span", attrs={"class": "top250-no"}).string[3:]
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    try:
        cur.execute(
            "update db_tops set year = %s,director = %s,screen_writer = %s,actor = %s,type = %s,time_long = %s,release_date = %s,intro = %s ,updated_at = %s  where no =%s",
            (year, director, screen_writer, actor, type, time_long, release_date, intro, dataTime, no))
        conn.commit()
    except Exception as err:
        print(err)
        exit(0)
    finally:
        cur.close()
        conn.close()

def main():
    hh = ['0','25','50','75','100','125','150','175','200','225','250']
    for h in hh:
        url = 'https://movie.douban.com/top250?start='+h+'&filter='
        node = getHtml(url)
        data_us,urls = parseList(node)
        listToMysql(data_us)
        parseUrl(urls)

    print('end')
    exit(0)
main()