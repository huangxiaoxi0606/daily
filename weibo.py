#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/17 12:23
# @Author : hhx06
# @Site : 
# @File : weibo.py
# @Software: PyCharm
# 1.几小时前改成日期
# 2.视频
# 3.多图
# 4.微博用户详情
from urllib.parse import quote,unquote
import requests
import json
import pymysql
import datetime

def getData(uid,luicode,pr,q,page,types):
    uid = uid
    luicode = luicode
    pr = pr
    mi = '1'
    q = q
    all = pr + 'type=' + mi + '&q=' + q
    lfid = quote(all, 'utf-8')
    type = 'uid'
    value = uid
    containerid = '107603' + uid
    page = page
    url = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode={}&lfid={}&type={}&value={}&containerid={}&page={}'.format(
        uid, luicode, lfid, type, value, containerid, page)
    response = requests.get(url=url)
    if types == 1:
        data = json.loads(response.text)['data']['cardlistInfo']['total']
    else:
        data = json.loads(response.text)['data']['cards']
    return data


def saveMysql(data):
    config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "root",
        "database": "hhx",
    }
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    # 连接数据库
    db = pymysql.connect(**config)
    cursor = db.cursor()

    for index in data:
        thumbnail_pic = original_pic = source = ''
        last_id = 0
        if 'retweeted_status' in index['mblog']:
            if 'thumbnail_pic' in index['mblog']:
                thumbnail_pic = index['mblog']['thumbnail_pic']
            if 'original_pic' in index['mblog']:
                original_pic = index['mblog']['original_pic']
            if 'source' in index['mblog']:
                source = index['mblog']['source']
            cursor.execute(
                "insert into weibos(text, thumbnail_pic, original_pic,source,weibo_created_at,comments_count,attitudes_count,reposts_count,scheme,screen_name,created_at,repost_id,is_flag)values"
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (index['mblog']['retweeted_status']['text'], thumbnail_pic, original_pic, source, index['mblog']['retweeted_status']['created_at'],
                 index['mblog']['retweeted_status']['comments_count'], index['mblog']['retweeted_status']['attitudes_count'], index['mblog']['retweeted_status']['reposts_count'],
                 '',index['mblog']['retweeted_status']['user']['screen_name'],
                 dataTime, 0,1))
            db.commit()
            last_id = cursor.lastrowid
        if 'thumbnail_pic' in index['mblog']:
            thumbnail_pic = index['mblog']['thumbnail_pic']
        if 'original_pic' in index['mblog']:
            original_pic = index['mblog']['original_pic']
        if 'source' in index['mblog']:
            source = index['mblog']['source']
        cursor.execute(
            "insert into weibos(text, thumbnail_pic, original_pic,source,weibo_created_at,comments_count,attitudes_count,reposts_count,scheme,screen_name,created_at,repost_id,is_flag)values"
            "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (index['mblog']['text'], thumbnail_pic, original_pic, source,
             index['mblog']['created_at'],
             index['mblog']['comments_count'],
             index['mblog']['attitudes_count'], index['mblog']['reposts_count'],
             index['scheme'], index['mblog']['user']['screen_name'],
             dataTime, last_id, 0))
        db.commit()
    cursor.close()
    db.close()

def main():
    uid = ''
    luicode = '10000011'
    pr = '100103'
    q = ''
    count = getData(uid, luicode, pr, q, 1,1)
    # print(count)
    # exit(0)
    h = int(count/10)+1
    for i in range(1,h):
        data = getData(uid, luicode, pr, q, i,0)
        if len(data) >0:
            saveMysql(data)
        print(i)
    print('完美结束')


if __name__ == '__main__':
    main()