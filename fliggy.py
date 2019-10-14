#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/17 14:46
# @Author : hhx06
# @Site : 
# @File : fliggy.py
# @Software: PyCharm
import requests
import time,datetime
import json
import pymysql

def getHtml(url):
    """
    获取数据
    :param url:
    :return:
    """
    response = requests.get(url)
    data_us = json.loads(response.text[6:-1])["data"]["flights"]
    return data_us

def parseData(data_us):
    """
    解析获得的数据
    :param data_us:
    :return:
    """
    data_info = []
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for data in data_us:
        data_info.append(
            [data['arrCode'], data['price'], data['discount'], data['arrName'], data['depName'], data['depDate'],
             data['priceDesc'], data['depCode'],dataTime])
    return data_info

def save_to_mysql(data_info):
    """
    保存数据库
    :param data_info:
    """
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    try:
        cur.executemany(
            "insert into flights(arrCode,price,discount,arrName,depName,depDate,priceDesc,depCode,created_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            data_info)
        conn.commit()
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()


def main():
    """
    未来30天郑州特价航班
    """
    today = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    startDate = today
    endDate = time.strftime("%Y-%m-%d",time.localtime(time.time()+3600*24*30))
    code = "CGO"
    url = 'https://r.fliggy.com/rule/domestic?startDate='+startDate+'&endDate='+endDate+'&routes='+code+'-&_ksTS=0&callback=jsonp&ruleId=99&flag=1'
    data_us = getHtml(url)
    data_info = parseData(data_us)
    save_to_mysql(data_info)
    print('end')

main()