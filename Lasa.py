#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/1 16:57
# @Author : hhx06
# @Site : 
# @File : Lasa.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://you.ctrip.com/travels/lhasa36/t3-p2.html'
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')