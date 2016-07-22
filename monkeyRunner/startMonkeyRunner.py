# -*- coding:utf-8 -*-
import os
import codecs
import time
from sys import argv

if(len(argv) == 2):
	category = argv[1]
else:
	category = ''
apkDir = 'D://javaDir/android/appAutoTest/downloadApk/apps/'+category+'/'#下载的apk保存的路径,改成你自己的路径
print(apkDir)

apkInfoDir = 'apkinfo/'#当前路径的apkinfo文件夹下，存储着apk解析信息

def apkList(apkDir):
	#查找指定目录下的所有apk文件，返回apk名的列表
	files = os.listdir(apkDir)
	apks = []
	for file in files:
		if file.split('.')[-1] == 'apk':
			apks.append(file)
	return apks

def installApk(apkPath):
	try:
		#执行安装命令
		cmd = 'adb install %s'%(apkPath)
		os.system(cmd)
	except Exception as e:
		return e

def getApkInfo(apkInfoDir,apkName):
	#解析apk包信息的程序和Monkey程序的异步处理
	#已经将apk信息保存在了某一目录的txt文件中，根据txt路径将指定apk的包名解析出来
	global category
	apkInfoPath = apkInfoDir+category+'_'+apkName+'.txt'
	#codecs防止编码错误
	with codecs.open('%s'%apkInfoPath,'r','utf-8') as f:
		lines = f.readlines()
	package = ''
	activity = ''
	for line in lines:
		if 'package' in line:
			package = (line.split("'"))[1]
		if 'launchable-activity' in line:
			activity = (line.split("'"))[1]
	return (package,activity)

def uninstallApk(pkgName):
	try:
		#执行卸载命令
		cmd = 'adb uninstall %s'%(pkgName)
		os.system(cmd)
	except Exception as e:
		return e

def monkeyRunner(package,activity):
	try:
		cmd = 'monkeyrunner run.py %s %s'%(package,activity)
		r = os.system(cmd)
	except Exception as e:
		return e
	if(r == 0):
		print('%s：MonkeyRunner批处理执行成功'%package)
	else:
		print('%s：MonkeyRunner批处理执行失败'%package)

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

def main():
	global apkDir,apkInfoDir

	apks = apkList(apkDir)
	for apkName in apks:
		apkPath = apkDir + apkName
		#installApk(apkPath)
		apkInfo = getApkInfo(apkInfoDir,apkName)
		monkeyRunner(apkInfo[0],apkInfo[1])
		pngDir = makePngDir(apkName)
		snapShot(pngDir,apkInfo[0],1)
		#uninstallApk(apkInfo[1])


if __name__ == '__main__':
	main()