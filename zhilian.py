#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2019-09-06 16:06
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
"""

"""
selenium, xpath爬取智联小爬虫

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree
from pymongo import MongoClient
from pymongo.results import InsertOneResult  # 一条条插入


class Zhilian:
    def __init__(self):
        # 设置无头浏览器
        self.brower = webdriver.Chrome()
        self.brower.set_window_size(1280, 1024)

    def get_url(self, url='https://www.zhaopin.com/', search='爬虫'):
        """
        爬取网页
        :param url:
        :param search:
        :return: html.text
        """
        self.brower.get(url)
        element = self.brower.find_element_by_xpath('//input[@class="zp-search__input"]')
        element.send_keys(f'{search}')
        time.sleep(1)
        element.send_keys(Keys.ENTER)
        # 切换窗口
        self.brower.switch_to.window(self.brower.window_handles[1])  # 跳转窗口
        time.sleep(4)
        html = self.brower.find_element_by_xpath("//*").get_attribute("outerHTML")  # 等待js渲染完成后，在获取html
        return html

    def data_process(self):
        """
        处理数据
        :return:dict
        """
        html = self.get_url()
        htmls = etree.HTML(html)

        jope_name = htmls.xpath(
            '//span[@class="contentpile__content__wrapper__item__info__box__jobname__title"]/@title')  # 工作名字
        # print(jope_name)
        company_name = htmls.xpath(
            '//a[@class="contentpile__content__wrapper__item__info__box__cname__title company_title"]/./@title')  # 公司名字
        # print(company_name)
        Salary = htmls.xpath('//p[@class="contentpile__content__wrapper__item__info__box__job__saray"]/text()')  # 薪金
        # print(Salary)
        year = htmls.xpath(
            '//li[@class="contentpile__content__wrapper__item__info__box__job__demand__item"][2]//text()')  # 工作经验
        # print(year)
        Education = htmls.xpath(
            '//li[@class="contentpile__content__wrapper__item__info__box__job__demand__item"][3]//text()')  # 学历
        # print(Education)
        # 构造字典
        zhilianlist = []
        for i in range(90):
            jop = {}
            jop['jope_name'] = jope_name[i]
            jop['company_name'] = company_name[i]
            jop['Salary'] = Salary[i]
            jop['year'] = year[i].strip()
            jop['Education'] = Education[i]
            zhilianlist.append(jop)
        # print(zhilianlist)
        # for i in zhilianlist:
        #     yield i
        return zhilianlist

    def save_mongo(self, dicts):
        client = MongoClient('mongodb://172.22.142.234:27017')
        db = client['zhilian']  # 指定数据库
        jops = db.zhilian  # 集合
        for i in dicts:
            x: InsertOneResult = jops.insert_one(i)
            print(x.inserted_id)



import time

if __name__ == '__main__':
    url = 'https://www.zhaopin.com/'
    sele = Zhilian()
    ss = sele.data_process()
    sele.save_mongo(ss)
