#!/bin/python3
#-*- coding:utf-8 -*-

import os
import re
import json
from selenium import webdriver


browser = webdriver.PhantomJS()
browser.set_window_size(1980,1140)
browser.set_page_load_timeout(120)

browser.get("http://data.eastmoney.com/notices/detail/000001/AN201801291083453496,JWU1JWI5JWIzJWU1JWFlJTg5JWU5JTkzJWI2JWU4JWExJThj.html")
file = open('D:\\Workspace\\notices-crawler\\demo-test\\test.txt','w+')
file.write(browser.page_source)
file.close()
print('done')

'''
file = open('D:\\Workspace\\notices-crawler\\demo-test\\test.txt','w+')
for item in items:
	print(item[0],item[1])
	#print(item.encode('utf-8'),item.encode('utf-8').decode('utf-8') + '\n')
	#file.write(item.encode('utf-8').decode('utf-8') + '\n')
file.close()
print("done")
#print(items)
'''

browser.quit()