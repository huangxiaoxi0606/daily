#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/4 17:13
# @Author : hhx06
# @Site : 
# @File : yl228.py
# @Software: PyCharm
import requests
import json
import pymysql
import time, datetime

def getData(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'Host': 'www.228.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.text
        return data


def writeMysql(data):
    config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "root",
        "database": "hhx",
    }
    # 连接数据库
    db = pymysql.connect(**config)
    cursor = db.cursor()
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for ar in data:
        count = cursor.execute("select * from yongles where performer='%s' and cityname ='%s'" % (ar['performer'],ar['cityname']))
        if count >0 :
            cursor.execute("update yongles set vname = %s, cityname=%s, prices=%s, enddate=%s, performer=%s,status =%s ,yname = %s, updated_at =%s  where cityname =%s and performer =%s",
                        (ar['vname'],ar['cityname'],ar['prices'],ar['enddate'],ar['performer'],ar['status'],ar['name'].strip(),dataTime,ar['cityname'],ar['performer']))
        else:
            cursor.execute("insert into yongles(vname, cityname, prices,enddate,performer,status,yname,created_at)values(%s, %s, %s, %s, %s, %s, %s,%s)",(ar['vname'],ar['cityname'],ar['prices'],ar['enddate'],ar['performer'],ar['status'],ar['name'].strip(),dataTime))
        db.commit()
    # else:
    # 多行插入
    cursor.close()
    db.close()


def main():
    name =''
    url = "https://www.228.com.cn/s/"+name + "/?j=1&p=1"
    data = (json.loads(getData(url))["products"])
    writeMysql(data)
    print('ya')

main()