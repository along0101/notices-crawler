#!/bin/python3
#-*- coding:utf-8 -*-

import os
import math
import time
import json
import pymysql


'''
特别说明：
导入文件没有去重复功能，所以请勿乱执行。基本用于第一次入库前就已经有文档备用了
因此使用完毕，请注释掉逻辑
'''


'''链接数据库'''
def connect_db():
    db = pymysql.connect(host="192.168.0.103", user="root",password="123456", db="chocolate", charset='utf8mb4', port=3007)
    return db



'''方案1 递归遍历'''
def gci(filepath):
#遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
    	fi_d = os.path.join(filepath,fi)
    	if os.path.isdir(fi_d):
    		gci(fi_d) 
    	else:
    		#print(os.path.join(filepath,fi_d))
    		print(os.path.join(fi_d))

#递归遍历./data目录下所有文件
#gci('./data')



if __name__ == '__main__':

	limit = 0
	InsertPerOnce = 5
	keys = "(org_code,org_name,title,digest,origin_url,publish_at,create_at)"
	sql = "insert into company_bulletin%s values" % keys
	now = math.floor(time.time())
	rows = []

	'''方案2 walk遍历'''
	for fpathe,dirs,fs in os.walk('./data'):
		for f in fs:
			filename = os.path.join(fpathe,f)
			try:
				print(filename)
				file = open(filename, encoding='utf-8', errors='ignore')
				data = json.loads(file.read(), strict=False)
				file.close()
				if hasattr(data,"publish_at"):
					date = data["publish_at"]
				else:
					date = "0000-00-00"
				
				row = '("%s","%s","%s","%s","%s","%s",%d)' % (data["org_code"],data["org_name"],data["title"],data["content"],data["origin_url"],date,now)
				rows.append(row)
				limit += 1
				if limit == InsertPerOnce:
					try:
						db = connect_db()
						with db.cursor() as cursor:
							cursor.execute(sql + ",".join(rows))
						db.commit()
						rows = []
						limit = 0
						print('insert %d rows' % InsertPerOnce)
					except Exception as e:
						db.rollback()
						print(e)
					finally:
						db.close()
				
			except Exception as e:
				'''
				file = open('./invalid-json.txt',"a",encoding='utf-8')
				file.write("file:%s ,reason:%s \n" % (filename , str(e)))
				file.close()
				'''
				print('except',e)

	#导入剩下的记录
	if rows:
		try:
			db = connect_db()
			with db.cursor() as cursor:
				cursor.execute(sql + ",".join(rows))
			db.commit()
			print('insert %d rows' % limit)
		except Exception as e:
			db.rollback()
			print(e)
		finally:
			db.close()

	print('done')

