#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/9 11:13
# @Author : hhx06
# @Site : 
# @File : weather.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import requests        #引用requests模块
r=requests.get('http://www.weather.com.cn/data/sk/101180101.html')       #获取
r.encoding='utf-8'   #编码
print("city:"+ r.json()['weatherinfo']['city'],"\nwendu:"+r.json()['weatherinfo']['temp'],"\nshidu:"+r.json()['weatherinfo']['SD'] ) #获取我们想要的信息
