#!/bin/python3
#-*- coding:utf-8 -*-

import os
import pymysql


'''链接数据库，获取股票代码列表'''
def get_stock_list():
    db = pymysql.connect(host="192.168.0.103", user="root", password="123456", db="chocolate", charset='utf8mb4', port=3007)

    sql = "select `real`,`code`,`name`,`status` from company where 1"

    with db.cursor() as cursor:
        cursor.execute(sql)
        stocks = cursor.fetchall()
    db.close()
    return stocks


stocks = get_stock_list()

i=0
for stock in stocks:
	file = open('./stocks.txt','a')
	file.write(",".join(str(s) for s in stock if s not in [None]) + '\n')
	file.close()
	i+=1
	print('line:%d'%i)
