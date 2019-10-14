#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/17 12:23
# @Author : hhx06
# @Site : 
# @File : weibo.py
# @Software: PyCharm

from urllib.parse import quote,unquote
import requests
import json
import pymysql
import datetime,time

def getData(url,type):
    response = requests.get(url=url)
    #1 获取用户信息:
    if type == 1:
        data = json.loads(response.text)['data']['userInfo']
    else:
        data = json.loads(response.text)['data']['cards']
    return data

# 微信内容存进mysql
def saveMysql(data,new):
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
        # if new['new'] == 0 and int(index['mblog']['id']) <= int(new['w_count']):
        #     print('无更新')
        #     exit(0)
        if 'mblog' in index:
            thumbnail_pic = original_pic = source = ''
            last_id = 0
            if 'retweeted_status' in index['mblog']:
                if 'thumbnail_pic' in index['mblog']['retweeted_status']:
                    thumbnail_pic = index['mblog']['retweeted_status']['thumbnail_pic']
                if 'original_pic' in index['mblog']['retweeted_status']:
                    original_pic = index['mblog']['retweeted_status']['original_pic']
                if 'source' in index['mblog']['retweeted_status']:
                    source = index['mblog']['retweeted_status']['source']
                zlen = len(index['mblog']['retweeted_status']['created_at'].split('-')) - 1
                if zlen == 2:
                    zb_created_at = index['mblog']['retweeted_status']['created_at']
                elif zlen == 1:
                    zb_created_at = str(datetime.datetime.now().year) + '-' + index['mblog']['retweeted_status']['created_at']
                else:
                    zb_created_at = datetime.date.today()

                if 'comments_count' in index['mblog']['retweeted_status']:
                    comments_count = index['mblog']['retweeted_status']['comments_count']
                else:
                    comments_count = 0
                if 'attitudes_count' in index['mblog']['retweeted_status']:
                    attitudes_count = index['mblog']['retweeted_status']['attitudes_count']
                else:
                    attitudes_count = 0
                if 'reposts_count' in index['mblog']['retweeted_status']:
                    reposts_count = index['mblog']['retweeted_status']['reposts_count']
                else:
                    reposts_count = 0
                hscreen_name = ''
                hid = 0

                if 'user' in index['mblog']['retweeted_status'] and index['mblog']['retweeted_status']['user']:
                    if 'screen_name' in index['mblog']['retweeted_status']['user']:
                        hscreen_name = index['mblog']['retweeted_status']['user']['screen_name']

                    if 'id' in index['mblog']['retweeted_status']['user']:
                        hid = index['mblog']['retweeted_status']['user']['id']
                cursor.execute(
                    "insert into weibos(text, thumbnail_pic, original_pic,source,weibo_created_at,comments_count,attitudes_count,reposts_count,scheme,screen_name,created_at,repost_id,is_flag,weibo_id,weibo_info_id)values"
                    "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (index['mblog']['retweeted_status']['text'], thumbnail_pic, original_pic, source, zb_created_at,
                     comments_count , attitudes_count, reposts_count,
                     '',hscreen_name,
                     dataTime, 0,1,hid,index['mblog']['retweeted_status']['id']))
                db.commit()
                last_id = cursor.lastrowid
            if 'thumbnail_pic' in index['mblog']:
                thumbnail_pic = index['mblog']['thumbnail_pic']
            if 'original_pic' in index['mblog']:
                original_pic = index['mblog']['original_pic']
            if 'source' in index['mblog']:
                source = index['mblog']['source']
            tlen = len(index['mblog']['created_at'].split('-'))-1
            if tlen == 2:
                wb_created_at = index['mblog']['created_at']
            elif tlen == 1:
                wb_created_at = str(datetime.datetime.now().year) + '-' + index['mblog']['created_at']
            else:
                wb_created_at = datetime.date.today()
            cursor.execute(
                "insert into weibos(text, thumbnail_pic, original_pic,source,weibo_created_at,comments_count,attitudes_count,reposts_count,scheme,screen_name,created_at,repost_id,is_flag,weibo_info_id,weibo_id,pic_num)values"
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (index['mblog']['text'], thumbnail_pic, original_pic, source,
                 wb_created_at,
                 index['mblog']['comments_count'],
                 index['mblog']['attitudes_count'], index['mblog']['reposts_count'],
                 index['scheme'], index['mblog']['user']['screen_name'],
                 dataTime, last_id, 0,index['mblog']['id'],index['mblog']['user']['id'],int(index['mblog']['pic_num'])))
            db.commit()
            # 大于1的时候
            if int(index['mblog']['pic_num']) > 1:
                for pic in index['mblog']['pics']:
                    cursor.execute(
                        "insert into weibo_pics(weibo_info_id,url,created_at)values"
                        "(%s,%s,%s)",
                        (index['mblog']['id'], pic['url'], dataTime))
                    db.commit()
            # else:
            #     # 保存视频
            #     if 'page_info' in index['mblog']:
            #         cursor.execute(
            #             "insert into weibo_videos(weibo_info_id,url,created_at)values"
            #             "(%s,%s,%s)",
            #             (index['mblog']['id'], index['mblog']['page_info']['page_url'], dataTime))
            #         db.commit()
    cursor.close()
    db.close()

# 用户信息存入数据库
def saveUserToMysql(data):
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
    count = cursor.execute(
        "select `weibo_id` from weibo_users where weibo_id='%s'" % (data['id']))
    if count == 0:
        cursor.execute(
            "insert into weibo_users(avatar_hd, cover_image_phone, description,follow_count,followers_count,gender,weibo_id,mbrank,mbtype,screen_name,statuses_count,created_at)values"
            "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (data['avatar_hd'],data['cover_image_phone'],data['description'],data['follow_count'],data['followers_count'],data['gender'],data['id'],data['mbrank'],data['mbtype'],data['screen_name'],data['statuses_count'],dataTime))
        db.commit()
        cursor.close()
        db.close()
        print('userInfo')
        print('isHave')
        return {'new': 1, 'w_count': 0}
    else:
        info_count = cursor.execute(
            "select `weibo_info_id` from weibos where weibo_id='%s' and is_flag ='%s'" % (data['id'], 0))
        if info_count == 0:
            info_id = 0
        else:
            info_id = cursor.fetchone()[0]
        return {'new': 0, 'w_count': info_id}


# 主程序
def main():
    # [uid :1751035982,q:田馥甄]
    # [uid :1836758555,q:Hhx_06]
    # [uid :1822796164,q:吴青峰]
    # [uid :1779763091,q:Yyy_07]
    # [uid :1698855832,q:暮以成风]


    uid = '1692801804'
    q = '楊千嬅'

    luicode = '10000011'
    all = '100103type= 1&q=' + q
    lfid = quote(all, 'utf-8')
    type = 'uid'
    value = uid
    # 用户信息
    containerid1 = '100505' + uid
    # 微博信息
    containerid2 = '107603' + uid
    url1 = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode={}&lfid={}&type={}&value={}&containerid={}'.format(
        uid, luicode, lfid, type, value, containerid1)
    data1 = getData(url1,1)
    new = saveUserToMysql(data1)
    count = data1['statuses_count']
    h = int(count/10)+1
    print(h)
    # h = 645
    # h = 80
    # 此处需解决数目大的时候
    for t in range(0, h,20):
        for i in range(t, t + 20):
            url2 = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode={}&lfid={}&type={}&value={}&containerid={}&page={}'.format(
                uid, luicode, lfid, type, value, containerid2, t)
            data2 = getData(url2,0)
            if len(data2) > 0:
                saveMysql(data2,new)
            time.sleep(5)
    print('endWeiBoInfo')
    exit(0)
if __name__ == '__main__':
    main()