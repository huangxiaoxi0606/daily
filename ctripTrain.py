#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/7/10 15:39
# @Author : hhx06
# @Site : 
# @File : ctripTrain.py
# @Software: PyCharm

import requests
from urllib.parse import urlencode
#未成功
def get_info_single_way(From, To, Date):
    """
    获取单程票信息
    :param From: 起点
    :param To: 终点
    :param Date: 出发日期
    :return:
    """
    base_url = 'http://trains.ctrip.com/TrainBooking/Search.aspx?'
    params1 = {
        'day': Date,
        'number': '',
        'fromDn': From.encode('gb2312'),
        'toCn': To.encode('gb2312')
    }
    Referer = base_url + urlencode(params1)

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '62',
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': 'Cookie:_abtest_userid=cc1bf074-b3ca-4908-8123-08a7909ab589; _ga=GA1.2.970578744.1562635990; MKT_Pagesource=PC; _RSG=35qHbmpmAy2kgO9sjbCVT9; _RDG=28404a76e9d1822b660723d2ec6fc24489; _RGUID=2f0ac33c-2547-4143-975f-325b76258aae; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; FD_SearchHistorty={"type":"S","data":"S%24%u90D1%u5DDE%28CGO%29%24CGO%242019-07-10%24%u62C9%u8428%28LXA%29%24LXA"}; MKT_OrderClick=ASID=4897155952&CT=1562731270643&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1562635989489.41xfch"}; gad_city=01e2fcd36d1bc003f51f35eff054dab1; _RF1=61.52.229.175; _gid=GA1.2.1107172219.1562893159; ASP.NET_SessionSvc=MTAuOC4xODkuNTh8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTU1NzgxMzQxNDE3Ng; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&Expires=1563499104556; _jzqco=%7C%7C%7C%7C1562731281346%7C1.203270096.1562636003610.1562893158838.1562894304564.1562893158838.1562894304564.undefined.0.0.11.11; _gat=1; __zpspc=9.6.1562894304.1562894406.2%232%7Csp0.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%25E7%2581%25AB%25E8%25BD%25A6%25E7%25A5%25A8%7C%23; _bfi=p1%3D108001%26p2%3D100101991%26v1%3D17%26v2%3D16; appFloatCnt=9; _bfa=1.1562635989489.41xfch.1.1562744165883.1562893155884.5.18; _bfs=1.6',
        'Host': 'trains.ctrip.com',
        'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
        'Origin': 'http://trains.ctrip.com',
        'Referer': Referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    data = {
        'value': {"dname": From, "aname": To, "ddate": Date}
    }
    params2 = {'Action': 'searchColudTickets'}
    url = 'http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?' + urlencode(params2)
    response = requests.post(url, data=data, headers=headers)
    print(response.content)

if __name__ == '__main__':
    get_info_single_way('成都', '上海', '2018-08-31')