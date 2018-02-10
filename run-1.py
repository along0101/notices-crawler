#!/bin/python3
#-*- coding:utf-8 -*-

import os
import re
from hashlib import md5
from collections import deque
import pymysql
from time import strftime, localtime, time, sleep,ctime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import './Crawler'
#from pybloomfilter import BloomFilter


'''
类封装版本 version modules

输出格式:{org_code,org_name,type=股东大会决议公告,title,digest,publish_at,prigin_url,create_at=time()}
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
'''


def request_logger(item):
    file = open("./log.txt",'a')
    file.write(",".join(item)+"\n")
    file.close()



if __name__ == '__main__':

    MAX_THREAD = 20
    CRAWL_DELAY = 0.5
    #threads = []

    crawler = Crawler()
    stocks = crawler.get_stock_list()

    for real, code, name, status in stocks:
        stock = real  # code[2:-1]
        for i in range(1, 20):
            stockurl = "http://data.eastmoney.com/notices/getdata.ashx?StockCode=%s&CodeType=1&PageIndex=%s&PageSize=50&rt=1517979419" % (
                stock, i)
            html_page = crawler.get_text(stockurl,3)
            #re.findall(r'"NOTICEDATE":"(199|200|201[0-9].*?)T.*?"Url":"(.*?)"}', html_page)
            #减少年份，获取2014至今的公告
            items = re.findall(r'"NOTICEDATE":"(201[4-9].*?)T.*?"Url":"(.*?)"}', html_page)
            for item in items:
                #date,url = item
                #print(date,url)
                #request_logger([code,date,url])
                crawler.request(item, [code, name], 3)

    crawler.close()

