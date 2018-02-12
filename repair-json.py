#!/bin/python3
#-*- coding:utf-8 -*-

import os
import math
import re
import time
import json


'''
特别说明：
json文件修复，用于修复下载的文件中
'''



if __name__ == '__main__':

	now = math.floor(time.time())
	count = 0

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
				raw_str = file.read()
				_str = raw_str.replace('{"', '').replace('"}', '').replace('":"', '","')
				_arr = _str.split('","')
				#todo
				new_str = re.sub(r'content:"(")','\"',raw_str)
				#file.write(new_str)
				file.close()
				
				fs = open("./test.json","w+",encoding="utf-8")
				fs.write(new_str)
				fs.close()
				time.sleep(300)

	print('done')

