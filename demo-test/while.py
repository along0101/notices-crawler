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


i = 0
while i < 5:
	try:
		#driver = init_browser()
		#http://data.eastmoney.com/notices/getdata.ashx?StockCode=000410&CodeType=1&PageIndex=1&PageSize=50&rt=1517979419
		print(ctime())
		driver.get("https://www.baidu.com/")
		print(driver.page_source)
	except Exception as e:
		i += 1
		print("error",'tries:',i)
	finally:
		#driver.quit()
		pass

driver.quit()