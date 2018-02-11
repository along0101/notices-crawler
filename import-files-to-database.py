#!/bin/python3
#-*- coding:utf-8 -*-

import os
import pymysql


#print(os.listdir('./data'))

'''
for path in os.listdir('./data'):
	if os.path.isdir(os.path.join(path)):
		print(path)
	else:
		print('is file')
'''


'''方案1'''
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


'''方案2'''
for fpathe,dirs,fs in os.walk('./data'):
	#print(fs)
	for f in fs:
		#print(os.path.join(fpathe,f))
		pass



'''
for dirpath, dirnames, filenames in os.walk('./data'):
	print(dirpath, dirnames, filenames)
'''