#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-07 10:03
# @Author  : Hhx03
# @Site    : 
# @File    : qunar.py
# @Software: PyCharm

import requests
import json
import pymysql
import time, datetime

def main():
    # url ='https://flight.qunar.com/touch/api/domestic/wbdflightlist?departureCity=%E9%83%91%E5%B7%9E&arrivalCity=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90&departureDate=2019-07-09&ex_track=&__m__=bac8c247f3f137ece2f75ce848473655&sort=&_v=4'
    url ='https://flight.qunar.com/touch/api/domestic/wbdflightlist?departureCity=郑州&arrivalCity=乌鲁木齐&departureDate=2019-07-10'
    response = requests.get(url)
    html = response.text
    data = json.loads(html)
    data_us = data["data"]["flights"];
    config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "",
        "database": "hhx",
    }
    # 连接数据库
    db = pymysql.connect(**config)
    cursor = db.cursor()
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for value in data_us:
        print(value["binfo"])
        count = cursor.execute(
            "select * from qunars where airCode='%s' and arrDate ='%s'" % (value["binfo"]['airCode'], value["binfo"]["arrDate"]))
        print(count)
        if count > 0:
            cursor.execute(
                "update qunars set airCode = %s, arrAirport=%s, arrAirportCode=%s, arrDate=%s, arrTerminal=%s,arrTime =%s ,crossDayDesc = %s, depDate =%s depAirport=%s depAirportCode=%s depTerminal=%s depTime=%s distance=%s flightTime=%s fullName=%s meal=%s piaoShao=%s planeFullType=%s shortCarrier=%s discountStr=%s minPrice=%s updated_at =%s  where airCode =%s and arrDate =%s ",
                (value["binfo"]['airCode'],value["binfo"]['arrAirport'],value["binfo"]['arrAirportCode'],value["binfo"]['arrDate'],value["binfo"]['arrTerminal'],value["binfo"]['arrTime'],value["binfo"]['crossDayDesc'],value["binfo"]["depDate"],value["binfo"]['depAirport'],value["binfo"]['depAirportCode'],value["binfo"]['depTerminal'],value["binfo"]['depTime'],value["binfo"]['distance'],value["binfo"]['flightTime'],value["binfo"]['fullName'],value["binfo"]['meal'],value["binfo"]['piaoShao'],value["binfo"]['planeFullType'],value["binfo"]['shortCarrier'],value['discountStr'],value['minPrice'],dataTime,value["binfo"]['airCode'], value["binfo"]['arrDate']))
        else:
            cursor.execute(
                "insert into qunars(airCode,arrAirport,arrAirportCode,arrDate,arrTerminal ,arrTime   ,crossDayDesc , depDate ,  depAirport,  depAirportCode,  depTerminal,  depTime,  distance,  flightTime,  fullName,  meal,  piaoShao,  planeFullType,  shortCarrier,  discountStr,  minPrice,  created_at)values(%s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s, %s, %s)",
                (value["binfo"]['airCode'],value["binfo"]['arrAirport'],value["binfo"]['arrAirportCode'],value["binfo"]['arrDate'],value["binfo"]['arrTerminal'],value["binfo"]['arrTime'],value["binfo"]['crossDayDesc'],value["binfo"]["depDate"],value["binfo"]['depAirport'],value["binfo"]['depAirportCode'],value["binfo"]['depTerminal'],value["binfo"]['depTime'],value["binfo"]['distance'],value["binfo"]['flightTime'],value["binfo"]['fullName'],value["binfo"]['meal'],value["binfo"]['piaoShao'],value["binfo"]['planeFullType'],value["binfo"]['shortCarrier'],value['discountStr'],value['minPrice'],dataTime))
        db.commit()
    cursor.close()
    db.close()
    print('22222')


# airCode,arrAirport,arrAirportCode,arrDate,arrTerminal ,arrTime   ,crossDayDesc , depDate ,  depAirport,  depAirportCode,  depTerminal,  depTime,  distance,  flightTime,  fullName,  meal,  piaoShao,  planeFullType,  shortCarrier,  discountStr,  minPrice,  updated_at ,

main()