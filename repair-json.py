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

#合并数组键=》值变成字典
#dict(zip(arr1,arr2))


if __name__ == '__main__':

	now = math.floor(time.time())
	count = 0

	for fpathe,dirs,fs in os.walk('./data'):
		for f in fs:
			filename = os.path.join(fpathe,f)
			try:
				file = open(filename, encoding='utf-8')
				#strict=False是允许字符串中出现\r \n
				json.loads(file.read(), strict=False)
				#data = json.loads(file.read())
				file.close()
			except Exception as e:
				'''专门修复异常的'''
				count += 1
				file = open(filename, 'r', encoding='utf-8')
				raw_str = file.read()
				file.close()
				_str = raw_str.replace('{"', '').replace('"}', '').replace('":"', '","')
				_arr = _str.split('","')
				_keys = []
				_values = []
				for i in range(len(_arr)):
					if i & 1:
						_values.append(_arr[i])
					else:
						_keys.append(_arr[i])

				_dict = dict(zip(_keys,_values))
				new_str = json.dumps(_dict,ensure_ascii=False)
				'''写回去'''
				file = open(filename, 'w', encoding='utf-8')
				file.write(new_str)
				file.close()
				print('fixed',filename)
				'''
				#用于测试观察
				fs = open("./test.json","w+",encoding="utf-8")
				fs.write(new_str)
				fs.close()
				time.sleep(300)
				'''
	print('done','fixed %d' % count)

