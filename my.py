#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/31 11:34
# @Author : hhx06
# @Site : 
# @File : my.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
import re


def main():
    url_pre = 'https://maoyan.com'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'Host': 'maoyan.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    url = url_pre + '/films/1230121'
    response = requests.get(url, headers=headers)
    node = BeautifulSoup(response.text, 'html.parser')
    banner = node.find('div', attrs={"class": "banner"})
    cover = banner.find('div', attrs={"class": "avatar-shadow"}).img['src']
    name = banner.find('h3', attrs={"class": "name"}).string+'/'+banner.find('div', attrs={"class": "ename"}).string
    ul = banner.find_all('li',attrs={"class": "ellipsis"})
    type = ul[0].string
    date = ul[2].string
    arr = ul[1].string.strip().split('/')
    area = arr[0]
    timelong = arr[1]
    # h = banner.find('span', attrs={"class": "info-num"})
    intro = node.find('span', attrs={"class": "dra"}).string
    director = node.find('ul', attrs={"class": "celebrity-list"}).get_text().strip()
    arrs = node.find_all('li', attrs={"class": "actor"})
    actor = ''
    for ar in arrs:
        actor = actor + ar.find('a', attrs={"class": "name"}).get_text().strip() + '/'
    hhx = []












def decrypt_font(url, headers):
    '''
    映射为构造成功
    输入：链接和头部信息
    输出：返回解决字体反爬后的页面源码
    '''

    font1 = TTFont('./fonts/base.woff')
    # 使用百度的FontEditor找到本地字体文件name和数字之间的对应关系, 保存到字典中
    base_dict = {'uniF30D': '0', 'uniE6A2': '8', 'uniEA94': '9', 'uniE9B1': '2', 'uniF620': '6',
                'uniEA56': '3', 'uniEF24': '1', 'uniF53E': '4', 'uniF170': '5', 'uniEE37': '7'}
    name_list1 = font1.getGlyphNames()[1:-1]
    response = requests.get(url, headers=headers).text
    # 正则匹配字体woff文件
    font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', response)[0]
    url2 = 'http://vfile.meituan.net/colorstone/' + font_file
    new_file = requests.get(url2, headers)
    with open('./fonts/' + font_file, 'wb') as f:
        f.write(new_file.content)
    font2 = TTFont('./fonts/' + font_file)
    font2.saveXML('./fonts/font_2.xml')
    name_list2 = font2.getGlyphNames()[1:-1]
    # 构造新映射
    new_dict = {}
    for name2 in name_list2:
        obj2 = font2['glyf'][name2]
        for name1 in name_list1:
            obj1 = font1['glyf'][name1]
            # 对象相等则说明对应的数字相同​
            if obj1 == obj2:
                new_dict[name2] = base_dict[name1]
    print(new_dict)
    exit(0)
    for i in name_list2:
        pattern = '&#x' + i[3:].lower() + ';'
        response = re.sub(pattern, new_dict[i], response)
    return response


main()