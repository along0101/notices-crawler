#!/bin/python3
#-*- coding:utf-8 -*-

import os,re,math,json
import pymysql
from hashlib import md5
from time import strftime, localtime, time, sleep,ctime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

'''
v1.0版，根据run-x.py一步步升级改造而来

特点：
1.快速过滤爬取过的页面记录
2.解决错误 [WinError 10054] <urlopen error [WinError 10061]
3.直接将数据录入数据库，并记录文件
'''



'''初始化浏览器，创建浏览器'''
def init_browser():
    cap = dict(DesiredCapabilities.CHROME)
    cap["version"] = "63.0.3239.84"
    cap["javascriptEnabled"] = False
    cap["loadImages"] = False
    #page.settings.userAgent
    #phantomjs.page.settings.loadImages
    cap["settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    cap["browser"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    driver = webdriver.PhantomJS(desired_capabilities=cap, service_args=['--load-images=no'])
    driver.set_page_load_timeout(15) #页面超时时间
    driver.set_window_size(1980, 1140)
    driver.implicitly_wait(15) #寻找一个元素的时间
    return driver

'''链接数据库'''
def connect_db():
    db = pymysql.connect(host="192.168.0.103", user="root",password="123456", db="chocolate", charset='utf8mb4', port=3007)
    return db



'''爬虫，用于爬取东方财富中的股票公告内容'''
class Crawler(object):

    request_count = 0
    driver = None
    db = None
    downloaded_urls = []
    dum_md5_file = "./download.txt"
    time_out_file = "./time_out.log"


    def __init__(self):
        super(Crawler, self).__init__()

        '''读取下载(爬取)记录'''
        try:
            self.dum_file = open(self.dum_md5_file, 'r', encoding='utf-8')
            self.downloaded_urls = self.dum_file.readlines()
            self.dum_file.close()
        except IOError:
            self.dum_file = open(self.dum_md5_file, 'a', encoding='utf-8')
            self.dum_file.close()
        self.driver = init_browser()
        self.db = connect_db()
        

    '''请求获取股票列表的数据'''
    def get_stock_list(self):
        sql = "select `real`,`code`,`name`,`status` from company where 1"
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            stocks = cursor.fetchall()
            self.db.close()
        self.stocks = stocks
        return self.stocks


    '''获取网页源代码内容'''
    def get_text(self, url, max_retries = 1):
        i = 0
        while i < max_retries:
            try:
                self.driver.get(url)
                html_page = self.driver.page_source
                return html_page
            except Exception as e:
                i += 1
                print('time_out,retries %d.' % i, date)
                '''记日志'''
                if max_retries == i:
                    print(e)
                    file = open(self.time_out_file, 'a', encoding='utf-8')
                    file.write('%s\n' % url)
                    file.close()
            finally:
                self.request_count += 1
                if self.request_count == 100:
                    self.request_count = 0
                    self.close()
                    self.open()
                    print('reopen phantom browser')
                    sleep(2)

    '''请求链接，打开页面'''
    def request(self, item, stock, max_retries = 1):
        i = 0
        while i < max_retries:
            try:
                date,url = item
                ymd = date.split("-")
                md5_url = md5(url.encode('utf-8')).hexdigest()
                #去重处理
                if md5_url + "\n" in self.downloaded_urls:
                    print("pass", date, url)
                    break

                self.driver.get(url)
                title = self.driver.find_element_by_css_selector('div.content.clearfix>div.cont_txt>div.detail-header>h1').text
                title = title.split(" ")[0]
                content = self.driver.find_element_by_css_selector("div.content.clearfix>div.cont_txt>div.detail-body>div:nth-child(1)").text
                pdfLink = self.driver.find_element_by_css_selector('div.cont_txt>div.detail-body>div:nth-child(2)>a').get_attribute("href")
                data = {"org_code":stock[0],"org_name":stock[1],"origin_url":pdfLink,"title":title,"content":content,"publish_at":date}
                
                fileName = md5_url + ".json"
                dir = './data/%s/%s/%s/' % (stock[0], ymd[0], "-".join(ymd[0:2]))
                if not os.path.exists(dir):
                    os.makedirs(dir)
                file = open(os.path.join(dir, fileName), 'w+', encoding='utf-8')
                file.write(json.dumps(data, ensure_ascii=False))
                file.close()

                print("success", stock[0], date)
                self.downloaded_urls.append(md5_url)
                #self.bloom_download_urls.add(md5_url)
                self.dum_file = open(self.dum_md5_file, 'a', encoding='utf-8')
                self.dum_file.write(md5_url + "\n")
                self.dum_file.close()
                break
            except Exception as e:
                i += 1
                print('time_out,retries %d.' % i, date)
                '''记日志'''
                if max_retries == i:
                    print(e)
                    file = open(self.time_out_file, 'a', encoding='utf-8')
                    file.write('%s\n' % url)
                    file.close()
            finally:
                self.request_count += 1
                if self.request_count == 100:
                    self.request_count = 0
                    self.close()
                    self.open()
                    print('reopen phantom browser')
                    sleep(2)


    '''打开浏览器'''
    def open(self):
        self.driver = init_browser()


    '''关闭浏览器'''
    def close(self):
        self.driver.quit()


'''
输出格式:{org_code,org_name,type=股东大会决议公告,title,digest,publish_at,origin_url,create_at=time()}
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
'''


if __name__ == '__main__':

    CRAWL_DELAY = 0.5
    _done = []
    _pages = []

    crawler = Crawler()
    stocks = crawler.get_stock_list()

    for real, code, name, status in stocks:
        stock = real  # code[2:-1]
        try:
            file = open("./crawled_stocks.txt", 'r', encoding='utf-8')
            _done = file.readlines()
            file.close()
        except Exception as e:
            file = open("./crawled_stocks.txt", 'a', encoding='utf-8')
            file.close()

        #跳过爬过的股票代码
        if stock + "\n" in _done:
            continue

        for i in range(1, 20):
            stockurl = "http://data.eastmoney.com/notices/getdata.ashx?StockCode=%s&CodeType=1&PageIndex=%s&PageSize=50&rt=1517979419" % (
                stock, i)
            md5_url = md5(stockurl.encode('utf-8')).hexdigest()

            try:
                file = open("./crawled_page.txt", "r", encoding='utf-8')
                _pages = file.readlines()
                file.close()
            except Exception as e:
                file = open("./crawled_page.txt", "a", encoding='utf-8')
                file.close()

            #跳过爬过的分页
            if md5_url + "\n" in _pages:
                continue

            '''
            re.findall(r'"NOTICEDATE":"(199|200|201[0-9].*?)T.*?"Url":"(.*?)"}', html_page)
            减少年份，获取2014至今的公告
            '''
            try:
                html_page = crawler.get_text(stockurl,3)
                items = re.findall(r'"NOTICEDATE":"(201[5-9].*?)T.*?"Url":"(.*?)"}', html_page)
                for item in items:
                    if item:
                        crawler.request(item, [code, name], 3)
                        sleep(CRAWL_DELAY)

                #记录爬取过的分页页面
                file = open("./crawled_page.txt", "a", encoding='utf-8')
                file.write('%s\n' % md5_url)
                file.close()
            except Exception as e:
                pass
            

        #记录爬取过的股票
        file = open("./crawled_stocks.txt", 'a', encoding='utf-8')
        file.write('%s\n' % stock)
        file.close()

    crawler.close()

