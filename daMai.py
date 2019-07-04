#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/4 12:03
# @Author : hhx06
# @Site : 
# @File : daMai.py
# @Software: PyCharm
import requests
import json
import csv
import pymysql
import time, datetime


# 获取页面html
def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None
# 获取总个数
def get_page_count(html):
    return json.loads(html)["pageData"]["maxTotalResults"]

# 获取数据
def get_data_all(html):
    return json.loads(html)["pageData"]["resultData"]

# 解析数据
def data_parse(data_us):
    arr = []
    for data_u in data_us:
        arr.append([data_u['cityname'], data_u['nameNoHtml'], data_u['price_str'],data_u['showtime'],data_u['venue'],data_u['showstatus']])
    return arr

# 写进csv
def write_csv(arr,name):
    with open(name+'data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['cityname', 'nameNoHtml', 'price_str', 'showtime', 'venue'])
        writer.writerows(arr)

#操作数据库
def write_mysql(name,arr):
    config ={
        "host": "127.0.0.1",
        "user": "root",
        "password":"root",
        "database":"hhx",
    }
    # 连接数据库
    db = pymysql.connect(**config)
    cursor = db.cursor()
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    # if row_count >0:
    for ar in arr:
        count = cursor.execute("select * from damais where actors='%s' and nameNoHtml ='%s'" % (name,ar[1]))
        if count >0 :
            cursor.execute("update damais set nameNoHtml = %s, cityname=%s, price_str=%s, showtime=%s, venue=%s,showstatus =%s, updated_at =%s  where actors =%s and nameNoHtml =%s",(ar[1],ar[0],ar[2],ar[3],ar[4],ar[5],dataTime,name,ar[1]))
        else:
            cursor.execute("insert into damais(actors, cityname, nameNoHtml,price_str,showtime,venue,showstatus,created_at)values(%s, %s, %s, %s, %s, %s, %s, %s)",(name,ar[0],ar[1],ar[2],ar[3],ar[4],ar[5],dataTime))
        db.commit()
    # else:
    # 多行插入
    cursor.close()
    db.close()

def main():
    url_prefix = 'https://search.damai.cn/searchajax.html?keyword='
    name = ''
    url_one = url_prefix + name +'&currPage=1&pageSize=30'
    url_two = url_prefix + name +'&currPage=1&pageSize='+ str(get_page_count(get_one_page(url_one)))
    data = data_parse(get_data_all(get_one_page(url_two)))
    write_mysql(name,data)
    print('success')

main()