#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 17:23
# @Author : hhx06
# @Site : 
# @File : cityTrain.py
# @Software: PyCharm
import re,requests

url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971"
response = requests.get(url,verify=False)
#将车站的名字和编码进行提取
chezhan = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
chezhan_code = dict(chezhan)

chezhan_names = dict(zip(chezhan_code.values(),chezhan_code.keys()))