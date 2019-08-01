#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/31 14:42
# @Author : hhx06
# @Site : 
# @File : travil.py
# @Software: PyCharm
# 携程热门游记100篇
import requests
import json
import datetime,time
from bs4 import BeautifulSoup
import pymysql
import re


def get_list(url, data):
    """
    获取列表
    :param url:
    :param data: 请求参数
    :return:
    """
    response = requests.post(url=url, data=data)
    data_us = json.loads(response.text)['Travel']
    travil_info = []
    url_info = []
    img_info = []
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for data in data_us:
        travil_info.append(
            [data['Author'], data['CommentNumber'], data['Content'], data['Img'], data['Name'], data['PublishDate'],
             data['PictureNumber'], data['TravelId'], data['ViewNumber'], data['Url'], dataTime])
        url_info.append([data['TravelId'], data['Url']])
        img_info.append([data['TravelId'], data['Img']])
    return travil_info, url_info,img_info


def save_to_mysql(travil_info):
    """
    列表解析数据存入数据库
    :param travil_info:
    """
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cur = conn.cursor()
    conn.select_db('hhx')
    try:
        cur.executemany(
            "insert into travils(Author,CommentNumber,Content,Img,Name,PublishDate,PictureNumber,TravelId,ViewNumber,Url,created_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            travil_info)
        conn.commit()
    except Exception as err:
        print(err)
    finally:
        cur.close()
        conn.close()


def get_info(url_info):
    """
    获取详情页
    :param url_info:
    """
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for data in url_info:
        url = data[1]
        response = requests.get(url)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'lxml')
        content = soup.find(class_='ctd_content').get_text("|", strip=True)
        img_info = []
        img = soup.find(class_='ctd_content').find_all('img')
        for i in img:
            img_url = i.attrs.get('data-original')
            if not img_url is None:
                img_info.append([data[0], img_url, dataTime])
        conn = pymysql.connect(host='localhost', user='root', password='root')
        cur = conn.cursor()
        conn.select_db('hhx')
        cur.execute("update travils set text = %s,updated_at =%s  where TravelId =%s",(content, dataTime, data[0]))
        conn.commit()
        try:
            cur.executemany(
                "insert into travil_pics(TravelId,ImgUrl,created_at) values(%s,%s,%s)",
                img_info)
            conn.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            conn.close()
        return img_info

def update_img_mysql(img_info):
    """
    图片更新到数据库
    :param img_info:
    """
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for img in img_info:
        fileName = download_img(img[1])
        fileNameInfo = '/storage/image/travil/'+fileName
        conn = pymysql.connect(host='localhost', user='root', password='root')
        cur = conn.cursor()
        conn.select_db('hhx')
        cur.execute("update travils set Img = %s ,updated_at= %s where TravelId =%s",(fileNameInfo, dataTime, img[0]))
        conn.commit()
        cur.close()
        conn.close()

def update_pic_mysql(img_info):
    """
    图片更新到数据库
    :param img_info:
    """
    now = datetime.datetime.now()
    dataTime = now.strftime("%Y-%m-%d %H:%M:%S")
    for img in img_info:
        fileName = download_img(img[1])
        fileNameInfo = '/storage/image/travil/' + fileName
        conn = pymysql.connect(host='localhost', user='root', password='root')
        cur = conn.cursor()
        conn.select_db('hhx')
        cur.execute("update travil_pics set ImgUrl = %s,updated_at = %s where TravelId = %s and ImgUrl = %s",(fileNameInfo, dataTime, img[0],img[1]))
        conn.commit()
        cur.close()
        conn.close()



def download_img(img_url):
    """
    下载远程图片到本地
    :param img_url:
    :return:
    """
    # img_url = 'https://youimg1.c-ctrip.com/target/fd/tg/g2/M07/5C/BF/Cghzf1WIGkuALVV8AAIyxYf9K4c696_R_671_10000_Q90.jpg'
    n = re.search(r'[^/]+$', img_url)
    m = re.search(r'.*\.jpg', n.group(0))
    fileName = m.group(0)
    path = 'D:\\laragon\\www\\hhx-admin\\public\\storage\\app\\public\\image\\travil\\' + fileName
    r = requests.get(img_url)
    print(r.status_code)  # 返回状态码
    if r.status_code == 200:
        open(path, 'wb').write(r.content)  # 将内容写入图片
        print("done")
    del r
    return fileName


def main():
    url = 'https://you.ctrip.com/yousite/Home/GetTravel'
    for i in range(1,10):
        data = {'traveltype': 'header',
                'pageindex': i}
        travil_info, url_info,img_info = get_list(url, data)
        save_to_mysql(travil_info)
        img_url = get_info(url_info)
        update_img_mysql(img_info)
        update_pic_mysql(img_url)
main()
