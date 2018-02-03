#coding utf-8
###!/bin/python
#说明：不够健壮，退市和不存在的股票没有节点选择，验证码手动输入都是错的。大约100个公司出现一次

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pymysql

#Chrome | Firefox | 
driver = webdriver.Chrome()

driver.get("http://www.cninfo.com.cn/cninfo-new/index#")

codeInput = driver.find_element_by_xpath('//*[@id="index_cw_input_obj"]')
tableSelect = Select(driver.find_element_by_xpath('//*[@id="index_select_type_obj"]'))
startYear = Select(driver.find_element_by_xpath('//*[@id="cw_start_select_obj"]'))
endYear = Select(driver.find_element_by_xpath('//*[@id="cw_end_select_obj"]'))
downloadBth = driver.find_element_by_xpath('//*[@id="con-f-2"]/div/div[4]/button')

#链接数据库
db = pymysql.connect(host="192.168.0.103",user="root",password="123456",db="chocolate",charset='utf8mb4',port=3007)


#sql = "select code,name from company where id>(select id from company where code='sz000033' limit 1)"
sql = "select code,name from company where id>(select id from company where code='sz000078' limit 1) and status=1"
with db.cursor() as cursor:
	cursor.execute(sql)
	stocks = cursor.fetchall()

db.close()

#driver.find_element_by_xpath("/html/body/div[3]/div[2]").click()


for symbol,name in stocks:
	code = symbol[2:8]
	#print(symbol,code,name)
	codeInput.clear()
	codeInput.send_keys(code)
	sleep(0.5)
	#prop = WebDriverWait(driver,5,05).until(EC.visibility_of(driver.find_element_by_xpath('//*[@id="index_cw_stock_list"]/li[2]/a'))
	prop = driver.find_element_by_xpath('//*[@id="index_cw_stock_list"]/li[2]/a')
	prop.click()
	#startYear.select_by_value("2016")
	endYear.select_by_value("2018")
	for index in range(0,3):
		tableSelect.select_by_index(index)
		sleep(0.5)
		downloadBth.click()
		sleep(1)
	sleep(2)
sleep(2)
driver.quit()
