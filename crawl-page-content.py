#-*- coding:utf-8 -*-
#!/bin/python3

from selenium import webdriver
from time import sleep
#from pybloomfilter import BloomFilter

#executable_path="D:\\DevTools\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe",
driver = webdriver.PhantomJS(service_args=['--load-images=no'])

#url = "http://data.eastmoney.com/notices/getdata.ashx?StockCode=？&CodeType=1&PageIndex=？&PageSize=50&rt=50239182"

driver.get("http://data.eastmoney.com/notices/detail/600660/AN201801081075113027,JWU3JWE2JThmJWU4JTgwJTgwJWU3JThlJWJiJWU3JTkyJTgz.html")

driver.set_window_size(1980,1140)

title = driver.find_element_by_css_selector('div.cont_txt>div.detail-header>h1').text

content = driver.find_element_by_css_selector("div.detail-body>div").text

pdfLink = driver.find_element_by_css_selector('div.cont_txt>div.detail-body>div:nth-child(2)>a').get_attribute("href")
#pdfLink = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[4]/div[1]/div[2]/div[2]/a').get_attribute("href")

#print(pdfLink,title)

#mode ['a','r','w']
file = open(r'D:\Workspace\notices-crawler\sh600660.txt','w+')
file.write('{"origin_url":"%s","title":"%s","content":"%s"}'%(pdfLink,title,content))

file.close()

#输出格式:{org_code,org_name,type=股东大会决议公告,title,digest,publish_at,prigin_url,create_at=time()}


driver.quit()