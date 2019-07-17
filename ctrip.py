#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/9 9:42
# @Author : hhx06
# @Site : 
# @File : ctrip.py
# @Software: PyCharm
import requests
import json
import pymysql
import time, datetime

def getHtml(url,data):
    response = requests.post(url=url, data=data)
    data_us = json.loads(response.text)
    data_u = data_us["data"]["oneWayPrice"][0]
    return data_u

def writeMysql(data_u,depAirportCode,arrAirportCode,depAirportName,arrAirportName):
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
    minValue = 2000
    minKey = '2019-08-07'
    min = '{v}:{k}'.format(v=minKey, k=minValue)
    count = cursor.execute(
        "select `minDate`,`minPrice` from ctrips where depAirportCode='%s' and arrAirportCode ='%s'" % (depAirportCode, arrAirportCode))
    ctrip = cursor.fetchone()
    if count >0:
        minValue = ctrip[0]
        minKey  = ctrip[1]
    for v, k in data_u.items():
        if (k < int(minValue)):
            minValue = k
            minKey = v
            min = '{v}:{k}'.format(v=v, k=k)
    print(min)
    if count >0:
        cursor.execute("update ctrips set minDate = %s, minPrice=%s,updated_at =%s  where depAirportCode =%s and arrAirportCode =%s",(minKey,minValue, dataTime,depAirportCode,arrAirportCode))
    else:
        cursor.execute("insert into ctrips(depAirportCode, arrAirportCode, depAirportName,arrAirportName,minDate,minPrice,created_at)values(%s, %s, %s, %s, %s, %s, %s)",(depAirportCode, arrAirportCode, depAirportName,arrAirportName,minKey,minValue,dataTime))
    db.commit()
    cursor.close()
    db.close()

def getData(depAirportCode,arrAirportCode,depAirportName,arrAirportName):
    url = 'https://flights.ctrip.com/itinerary/api/12808/lowestPrice'
    data = {"flightWay": "Oneway",
            "dcity": depAirportCode,
            "acity": arrAirportCode,
            "army": "false"}
    data_u = getHtml(url, data)
    writeMysql(data_u, depAirportCode, arrAirportCode, depAirportName, arrAirportName)

def getParam():
    config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "root",
        "database": "hhx",
    }
    # 连接数据库
    db = pymysql.connect(**config)
    cursor = db.cursor()
    cursor.execute("select `depAirportCode`,`arrAirportCode`,`depAirportName`,`arrAirportName` from ctrips where status='%d'" % (1))
    ctrips = cursor.fetchall()
    if len(ctrips) != 0:
       for arr in ctrips:
           depAirportCode = arr[0]
           arrAirportCode = arr[1]
           depAirportName = arr[2]
           arrAirportName = arr[3]
           getData(depAirportCode, arrAirportCode, depAirportName, arrAirportName)

    cursor.close()
    db.close()

def paramsRequest():
    depAirportCode = "cgo"
    arrAirportCode = "urc"
    depAirportName = "郑州"
    arrAirportName = "乌鲁木齐"
    getData(depAirportCode, arrAirportCode, depAirportName, arrAirportName)

def main():
    # paramsRequest()
    getParam()
    #

if __name__ == '__main__':
    main()