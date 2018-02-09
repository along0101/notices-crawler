#!/bin/python3
#-*- coding:utf-8 -*-

from time import ctime
from selenium import webdriver

#service_args=['--load-images=no']
driver = webdriver.PhantomJS()
driver.set_page_load_timeout(5)



def init_browser():
	driver = webdriver.PhantomJS(service_args=['--load-images=no'])
	driver.set_page_load_timeout(10)
	return driver



def get_text(url,max_retries=1):
	i = 0
	while i < max_retries:
		try:
			#driver = init_browser()
			print(ctime())
			driver.get(url)
			return driver.page_source
		except Exception as e:
			i += 1
			print("error",'tries:',i)

#http://data.eastmoney.com/notices/getdata.ashx?StockCode=000410&CodeType=1&PageIndex=1&PageSize=50&rt=1517979419
#https://www.baidu.com/

html = get_text("https://dev.xdreport123.com/",3)
print('done')

driver.quit()