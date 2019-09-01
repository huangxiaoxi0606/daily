#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-08-25 21:23
# @Author  : Hhx03
# @Site    : 
# @File    : qyer.py
# @Software: PyCharm
import requests
import json
import pymysql
import datetime,time

def getData(url):
    response = requests.get(url)
    if response.status_code == 200:
        data_us = json.loads(response.text)['data']['list']
    return data_us

def getParse(data_us):

    arr = []
    urls = []
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for data_u in data_us:
        arr.append([data_u['id'], data_u['face'], data_u['forumsname'], data_u['image'], data_u['last_post_time'],
                    data_u['likeNumber'], data_u['post'], data_u['subject'], data_u['total_replies'], data_u['type'],
                    data_u['typename'], data_u['username'], data_u['viewNumber'], data_u['url'],dataTime])
        urls.append(data_u['url'])
    return arr,urls

def saveToMysql(arr):
    conn = pymysql.connect(host='localhost', user='root', password ='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    cur.executemany("insert into qyers(post_id,face,forumsname,image,last_post_time,likeNumber,post,subject,total_replies,type,typename,username,viewNumber,url,created_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",arr)
    conn.commit()
    cur.close()
    conn.close()





def main():
    for i in range(1,7):

        page = i
        url = 'https://bbs.qyer.com/index.php?action=getTravels&page=' + str(page)
        data_us = getData(url)
        arr,urls = getParse(data_us)
        # arr保存进数据库 urls继续解析
        saveToMysql(arr)





    # print(data_us)
    exit(0)


if __name__ == '__main__':
    main()