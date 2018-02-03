#coding utf-8
###!/bin/python

from selenium import webdriver
from time import sleep


driver = webdriver.Firefox()

driver.get("http://baidu.com")

driver.find_element_by_xpath('//*[@id="kw"]').send_keys("selenium")
driver.find_element_by_xpath('//*[@id="su"]').click()

sleep(10)

driver.quit()
