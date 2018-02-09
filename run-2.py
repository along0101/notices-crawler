#!/bin/python3
#-*- coding:utf-8 -*-

import os
import re
from hashlib import md5
import pymysql
from time import strftime, localtime, time, sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from pybloomfilter import BloomFilter


cap = dict(DesiredCapabilities.PHANTOMJS)
cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
cap["phantomjs.page.settings.loadImages"] = False

driver = webdriver.PhantomJS(desired_capabilities=cap, service_args=['--load-images=no'])
'''页面超时时间'''
driver.set_page_load_timeout(30)
driver.set_window_size(1980, 1140)
'''寻找一个元素的时间'''
driver.implicitly_wait(20)


'''获取网页源代码内容'''
def get_text(url,max_retries = 1):
    i = 0
    while i < max_retries:
        try:
            driver.get(url)
            html_page = driver.page_source
            return html_page;
        except Exception as e:
            i += 1
            print('time_out,it would try %d times,current %d.' % ( max_retries, i))
            '''记一下日志'''
            file = open('./data/fail.log', 'a')
            file.write('tries:%d,url:%s\n' % (i, url))
            file.close()



'''链接数据库，获取股票代码列表'''
def get_stock_list():
    db = pymysql.connect(host="192.168.0.103", user="root",
                     password="123456", db="chocolate", charset='utf8mb4', port=3007)

    sql = "select `real`,`code`,`name`,`status` from company where 1"

    with db.cursor() as cursor:
        cursor.execute(sql)
        stocks = cursor.fetchall()
    db.close()
    return stocks


stocks = get_stock_list()



#title = driver.find_element_by_css_selector('div.cont_txt>div.detail-header>h1').text
#content = driver.find_element_by_css_selector("div.detail-body>div").text
#pdfLink = driver.find_element_by_css_selector('div.cont_txt>div.detail-body>div:nth-child(2)>a').get_attribute("href")
# 输出格式:{org_code,org_name,type=股东大会决议公告,title,digest,publish_at,prigin_url,create_at=time()}

#print(strftime('%Y-%m-%d %H:%M:%S', localtime()))

for real, code, name, status in stocks:
    stock = real  # code[2:-1]
    for i in range(1, 20):
        stockurl = "http://data.eastmoney.com/notices/getdata.ashx?StockCode=%s&CodeType=1&PageIndex=%s&PageSize=50&rt=1517979419" % (
            stock, i)
        html_page = get_text(stockurl,3)
        items = re.findall(
            r'"NOTICEDATE":"(199|200|201[0-9].*?)T.*?"Url":"(.*?)"}', html_page)
        for item in items:
            date,url = item
            tries = 3

            #driver.get(url)
            print(date,url)
            file = open(code + '_download_url.txt', 'a')
            file.write('{"org_code":"%s","org_name":"%s","date":"%s","url":"%s"}\n' % (
                    code, name, date, url))
            file.close()
            '''
            try:
                title = driver.find_element_by_css_selector(
                    'div.content.clearfix>div.cont_txt>div.detail-header>h1').text
                content = driver.find_element_by_css_selector(
                    "div.content.clearfix>div.cont_txt>div.detail-body>div:nth-child(1)").text
                pdfLink = driver.find_element_by_css_selector(
                    'div.cont_txt>div.detail-body>div:nth-child(2)>a').get_attribute("href")
                ymd = date.split("-")
                fileName = md5(url.encode('utf-8')).hexdigest() + ".txt"
                dir = 'D:\\Workspace\\notices-crawler\\data\\%s\\%s\\%s\\' % (
                    stock, ymd[0], "-".join(ymd[0:2]))
                if not os.path.exists(dir):
                    os.makedirs(dir)
                file = open(os.path.join(dir, fileName), 'w+')
                file.write('{"org_code":"%s","org_name":"%s","origin_url":"%s","title":"%s","content":"%s"}' % (
                    code, name, pdfLink, title, content))
                file.close()
                # crawler.enqueueUrl(item)
            except NoSuchElementException as e:
                print(e)
            finally:
                # file.close()
                break
            '''
driver.quit()
