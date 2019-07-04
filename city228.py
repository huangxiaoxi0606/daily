#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/4 16:23
# @Author : hhx06
# @Site : 
# @File : city228.py
# @Software: PyCharm
import requests
import json
import pymysql

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
    # 多个插入 错误
    # cursor.executemany()
    for data_us in data:
        cursor.execute(
            "insert into ylcities(CITYJX, CITYNAME, DISTRICTID,PRODUCTNUM)values(%s, %s, %s,%s)",(data_us['CITYJX'],data_us['CITYNAME'].strip(),data_us['DISTRICTID'],data_us['PRODUCTNUM']))
        db.commit()
    cursor.close()
    db.close()

def main():
    url = "https://www.228.com.cn/ajax/findpronum.json?nc=30"
    data = (json.loads(getData(url))["fcitys"])
    writeMysql(data)
    print('ok')



main()