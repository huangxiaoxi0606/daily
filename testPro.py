#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/26 9:04
# @Author : hhx06
# @Site : 
# @File : testPro.py
# @Software: PyCharm
import requests


proxies = {
  "http": "http://121.15.254.156:888",
}
def main():
    url = 'http://music.163.com/api/song/lyric?id=1374061028&lv=1&kv=1&tv=-1'
    r = requests.get(url,proxies=proxies)
    print(r.text)

main()