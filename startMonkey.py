#!/usr/bin/env python
# coding=utf-8

'''
此测试脚本基于adb的几个命令：
adb install {apkPath}——安装apk
adb uninstall -p {pkgName}——卸载app
adb shell monkey -p {pkgName} -vvv 100——给设备上指定包名的app发送100个随机事件流
adb shell /system/bin/screencap -p /sdcard/temp.png——给安卓设备截屏并保存到sd卡
adb pull /sdcard/temp.png {pngPath}——将安卓设备上的图片传入到电脑的指定路径中
'''
import os
import time
import codecs
from threading import Thread
from sys import argv

try:
	#在命令行参数输入下载的apk保存的绝对路径
	apkDir = argv[1]
	if(apkDir[-1]) != '/'):
		apkDir += '/'
except:
	exit('Please add apk absolute path')
	
#apkDir = 'D://javaDir/android/appAutoTest/downloadApk/'
pngNum = 30#每个app截屏的数量
eventNum = 20#每次截屏之前进行的伪随机事件数
apkInfoDir = 'apkinfo/'#当前路径的apkinfo文件夹下，存储着apk解析信息

def apkList(apkDir):
	#查找指定目录下的所有apk文件，返回apk名的列表
	files = os.listdir(apkDir)
	apks = []
	for file in files:
		if file.split('.')[-1] == 'apk':
			apks.append(file)
	return apks

def installApk(apkDir,apkName):
	apkPath = apkDir+apkName
	try:
		#执行安装命令
		cmd = 'adb install %s'%(apkPath)
		os.system(cmd)
	except Exception as e:
		return e

def getApkPkgName(apkInfoDir,apkName):
	#解析apk包信息的程序和Monkey程序的异步处理
	#已经将apk信息保存在了某一目录的txt文件中，根据txt路径将指定apk的包名解析出来
	apkInfoPath = apkInfoDir+apkName+'.txt'
	#codecs防止编码错误
	with codecs.open('%s'%apkInfoPath,'r','utf-8') as f:
		lines = f.readlines()
	for line in lines:
		if 'package' in line:
			package = (line.split("'"))[1]
			return package
	return

def uninstallApk(pkgName):
	try:
		#执行卸载命令
		cmd = 'adb uninstall %s'%(pkgName)
		os.system(cmd)
	except Exception as e:
		return e


def runMonkey(pkgName):
	global eventNum
	seed = int(time.time())
	try:
		#执行monkey命令
		cmd = 'adb shell monkey -p %s -s %d -vvv %d'%(pkgName,seed,eventNum)
		os.system(cmd)
	except Exception as e:
		return e


def snapShot(pngDir,pkgName,i):
	savePath = pngDir+'/'+pkgName+str(i)+'.png'
	try:
		#执行截屏命令并传输到电脑的指定路径中
		cmd1 = 'adb shell /system/bin/screencap -p /sdcard/temp%d.png'%(i)
		os.system(cmd1)
		cmd2 = 'adb pull /sdcard/temp%d.png %s'%(i,savePath)
		os.system(cmd2)
	except Exception as e:
		return e

def makePngDir(apkName):
	pngDir = '%s_snapShot'%apkName
	if not os.path.exists(pngDir):
		os.mkdir(pngDir)
		
	return pngDir


def run(apkName):
	global pngNum,apkDir,apkInfoDir

	installApk(apkDir,apkName)
	time.sleep(1)
	pkgName = getApkPkgName(apkInfoDir,apkName)
	pngDir = makePngDir(apkName)
	for i in range(pngNum):
		runMonkey(pkgName)
		snapShot(pngDir,pkgName,i)
	uninstallApk(pkgName)

def main():
	global apkDir
	apks = apkList(apkDir)
	threads = []
	for apkName in apks:
		t = Thread(target=run,args=(apkName,))
		threads.append(t)

	for t in threads:
		t.start()
	t.join()


if __name__ == '__main__':
	main()
