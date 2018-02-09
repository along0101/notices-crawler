#!/bin/python3
#-*- coding:utf-8 -*-

import os
import re
from hashlib import md5
import pymysql
from time import strftime, localtime, time, sleep,ctime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from pybloomfilter import BloomFilter


class Crawler(object):
    """
    爬虫，用于爬取东方财富中的股票公告内容
    """
    downloaded_urls = []
    dum_md5_file = "./download.txt"
    time_out_file = "./data/time_out.log"

    def __init__(self):
        super(Crawler, self).__init__()
        cap = dict(DesiredCapabilities.PHANTOMJS)
        cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        cap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=cap, service_args=['--load-images=no'])
        '''页面超时时间'''
        self.driver.set_page_load_timeout(10)
        self.driver.set_window_size(1980, 1140)
        '''寻找一个元素的时间'''
        self.driver.implicitly_wait(5)
        

    '''请求获取股票列表的数据'''
    def get_stock_list(self):
        db = pymysql.connect(host="192.168.0.103", user="root",
                     password="123456", db="chocolate", charset='utf8mb4', port=3007)

        sql = "select `real`,`code`,`name`,`status` from company where 1"

        with db.cursor() as cursor:
            cursor.execute(sql)
            stocks = cursor.fetchall()
        db.close()
        self.stocks = stocks
        return self.stocks


    '''获取网页源代码内容'''
    def get_text(self,url,max_retries = 1):
        i = 0
        while i < max_retries:
            try:
                self.driver.get(url)
                html_page = self.driver.page_source
                return html_page
            except Exception as e:
                i += 1
                #print(e)
                print('time_out,retries %d.' %i)
                '''记一下日志'''
                if max_retries == i:
                    file = open(self.time_out_file, 'a')
                    file.write('%s\n' % url)
                    file.close()

    '''请求链接，打开页面'''
    def request(self,item,stock,max_retries = 1):
        i = 0
        while i < max_retries:
            try:
                self.driver.get(item[1])
                title = self.driver.find_element_by_css_selector('div.content.clearfix>div.cont_txt>div.detail-header>h1').text
                content = self.driver.find_element_by_css_selector("div.content.clearfix>div.cont_txt>div.detail-body>div:nth-child(1)").text
                pdfLink = self.driver.find_element_by_css_selector('div.cont_txt>div.detail-body>div:nth-child(2)>a').get_attribute("href")
                ymd = item[0].split("-")
                fileName = md5(item[1].encode('utf-8')).hexdigest() + ".json"
                dir = 'D:\\Workspace\\notices-crawler\\data\\%s\\%s\\%s\\' % (stock[0], ymd[0], "-".join(ymd[0:2]))
                if not os.path.exists(dir):
                    os.makedirs(dir)
                file = open(os.path.join(dir, fileName), 'w+')
                file.write('{"org_code":"%s","org_name":"%s","origin_url":"%s","title":"%s","content":"%s"}' % (stock[0], stock[1], pdfLink, title, content))
                file.close()
                print("success",stock[0],item[0])
                break
            except Exception as e:
                i += 1
                #print(e)
                print('time_out,retries %d.' %i,item[0])
                '''记一下日志'''
                if max_retries == i:
                    file = open(self.time_out_file, 'a')
                    file.write('%s\n' % item[1])
                    file.close()


    def close(self):
        self.driver.quit()


# 输出格式:{org_code,org_name,type=股东大会决议公告,title,digest,publish_at,prigin_url,create_at=time()}
#print(strftime('%Y-%m-%d %H:%M:%S', localtime()))

def request_logger(item):
    file = open("./log.txt",'a')
    file.write(",".join(item)+"\n")
    file.close()



if __name__ == '__main__':

    crawler = Crawler()
    stocks = crawler.get_stock_list()

    for real, code, name, status in stocks:
        stock = real  # code[2:-1]
        for i in range(1, 20):
            stockurl = "http://data.eastmoney.com/notices/getdata.ashx?StockCode=%s&CodeType=1&PageIndex=%s&PageSize=50&rt=1517979419" % (
                stock, i)
            html_page = crawler.get_text(stockurl,3)
            items = re.findall(r'"NOTICEDATE":"(199|200|201[0-9].*?)T.*?"Url":"(.*?)"}', html_page)
            for item in items:
                #date,url = item
                #print(date,url)
                #request_logger([code,date,url])
                crawler.request(item, [code, name], 3)

    crawler.close()

