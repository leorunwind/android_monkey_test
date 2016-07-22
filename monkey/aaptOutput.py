# -*- coding:utf-8 -*-
'''
该脚本将apk解析信息保存到当前路径的apkinfo文件夹下
'''
import os
from threading import Thread

category = '新闻资讯'
apkDir = 'D://javaDir/android/appAutoTest/downloadApk/apps/'+category+'/'#下载的apk保存的路径,改成你自己的路径

def apkList(apkDir):
	#查找指定目录下的所有apk文件，返回apk名的列表
	files = os.listdir(apkDir)
	apks = []
	for file in files:
		if file.split('.')[-1] == 'apk':
			apks.append(file)
	return apks

def aaptOutput(apkDir,apkName):
	#将apk解析信息保存在apkinfo文件夹下的txt里，用于获得包名等信息
	apkPath = apkDir+apkName
	try:
		#执行aapt命令获取apk信息并保存到apkinfo文件夹下的txt里
		cmd = 'aapt dump badging %s > apkinfo/%s_%s.txt'%(apkPath,category,apkName)
		r = os.popen(cmd)
	except Exception as e:
		return e
	return '%s resolved successfully!'%apkName


def main():
	global apkDir
	threads = []

	if not os.path.exists('apkinfo'):
		#在当前路径创建apkinfo文件夹，用于存储apk解析信息
		os.mkdir('apkinfo')

	apks = apkList(apkDir)
	for apkName in apks:
		t = Thread(target=aaptOutput,args=(apkDir,apkName))
		threads.append(t)
	for t in threads:
		t.start()
	t.join()

if __name__ == '__main__':
	main()