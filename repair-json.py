#!/bin/python3
#-*- coding:utf-8 -*-

import os
import math
import time
import json


'''
特别说明：
json文件修复，用于修复下载的文件中
'''




if __name__ == '__main__':

	now = math.floor(time.time())
	count = 0

	'''方案2 walk遍历'''
	for fpathe,dirs,fs in os.walk('./data'):
		for f in fs:
			filename = os.path.join(fpathe,f)
			try:
				#print(filename)
				file = open(filename, encoding='utf-8')
				#strict=False是允许字符串中出现\r \n
				json.loads(file.read(), strict=False)
				#data = json.loads(file.read())
				file.close()
			except Exception as e:
				'''专门修复异常的'''
				file = open(filename, encoding='utf-8')
				content_string = file.read()
				file.close()
				count +=1
				print(count)
				'''
				file = open('./invalid-json.txt',"a",encoding='utf-8')
				file.write("file:%s ,reason:%s \n" % (filename , str(e)))
				file.close()
				'''
				#print('except',e)
				pass


	print('done')

