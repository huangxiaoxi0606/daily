#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/10 15:39
# @Author : hhx06
# @Site : 
# @File : ctripTrain.py
# @Software: PyCharm

import requests
import json

def main():
    url = 'https://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=searchColudTickets'
    value = {"dname":"郑州","aname":"长沙","ddate":"2019-07-11"}
    response = requests.post(url=url, data=value)




if __name__ == '__main__':
    main()