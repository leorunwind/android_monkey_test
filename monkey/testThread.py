# -*- coding:utf-8 -*-
'''
该脚本将apk解析信息保存到当前路径的apkinfo文件夹下
'''
import time
from threading import Thread
import os

def test(i,j):
	time.sleep(0.3)
	print('%d:threading %d is running'%(i,j))

def main():
	threads = []
	for i in range(1,11):
		j = i
		t = Thread(target=test,args=(i,j))
		threads.append(t)
	
	for t in threads:
		t.start()
	t.join()
	print('end')

def main1():
	for i in range(1,11):
		test(i)

def pwd():
	print(os.path.abspath('apkinfo').replace('\\','/'))

if __name__ == '__main__':
	#start = time.time()
	#main1()
	#print('running time:',time.time()-start)
	start = time.time()
	main()
	print('running time:',time.time()-start)
	pwd()