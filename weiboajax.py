#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2019-09-06 16:18
# Author : chenkeke
# E-mail: 502244366@qq.com
"""
/**********/**********/**********//**********//**********//**********//**********/
  .--,       .--,
 ( (  \.---./  ) )
  '.__/o   o\__.'
     {=  ^  =}
      >  -  <
     /       \
    //       \\
   //|   .   |\\
   "'\       /'"_.-~^`'-.
      \  _  /--'         `
    ___)( )(___
   (((__) (__)))    高山仰止,景行行止.虽不能至,心向往之。



/**********/**********/**********//**********//**********//**********//**********/
分析微博，通过Ajax实现微博发过信息的爬取
"""

import requests
from urllib.parse import urlencode
from jsonpath import jsonpath
import re
from pyquery import PyQuery as pd

# type=uid&value=2830678474&containerid=1076032830678474&page=2
base_url = 'https://m.weibo.cn/api/container/getIndex?'
# 构建请求头
headers = {
    'Host': 'm.weibo.cn',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'referer': 'https://m.weibo.cn/u/2830678474'
}


def get_page(page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url + urlencode(params)
    print(url)
    return url


def get_html(url):
    response = requests.get(url, headers=headers, verify=False)  # 解决ssl的问题
    html = response.json()  # 因为是json格式的，所以要转为python的字符串格式
    time.sleep(1)
    return html if str(response.status_code).startswith('2') else print('Error')


def parses(html: dict):
    """
    保存微博的 id、正文、赞数、评论数和转发数这几个内容
    :param html:
    :return: ID：id 正文：text,attitudes_count 赞数, comments_count 评论数,reposts_count 转发数
    """
    if html:
        items = html.get('data').get('cards')  # 指定取data下的cards的mblog,返回的是一个List
        ss = []
        for item in items:
            item = item.get('mblog')
            alldata = {}
            alldata['id'] = item.get('id')
            alldata['text'] = pd(item.get('text')).text()  # 用pyquery处理文本问题
            alldata['attitudes_count'] = item.get('attitudes_count')
            alldata['comments_count'] = item.get('comments_count')
            alldata['reposts_count'] = item.get('reposts_count')
            yield alldata
        #     ss.append(alldata)
        # print(len(ss))

from pymongo import MongoClient
from pymongo.results import InsertOneResult


def save_mongodb(ss):
    client = MongoClient('mongodb://172.16.6.139:27017')
    db = client['weibo']  # 指定数据库
    jj = db.weibo  # 集合
    for i in ss:
        x: InsertOneResult = jj.insert_one(i)
        print(x.inserted_id)


import time

if __name__ == '__main__':
    for page in range(1, 10):
        html = get_page(page)  # 1的page对应的是2
        html_json = get_html(html)
        ss = parses(html_json)
        save_mongodb(ss)
