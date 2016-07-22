# -*- coding:UTF-8 -*-
from com.android.monkeyrunner import MonkeyRunner
from com.android.monkeyrunner import MonkeyDevice
import logging
import time
from sys import argv

big = 0
small = 0
incX = 0
incY = 0
beginX = 0
beginY = 0
results = []
device = None

#日志信息
log=logging.getLogger()
handler=logging.FileHandler('mrTest/log.txt')
log.addHandler(handler)
log.setLevel(logging.NOTSET)

def logInfo(msg):
    log.info('[info] '+time.strftime('%Y-%m-%d %X')+' '+msg)

def logWarn(msg):
    log.warn('[warn] '+time.strftime('%Y-%m-%d %X')+' '+msg)

def logError(msg):
    log.error('[error] '+time.strftime('%Y-%m-%d %X')+' '+msg)
#log.removeHandler(handler)

def deviceInit():
    device = MonkeyRunner.waitForConnection()
    runComponent = argv[1]+'/'+argv[2]
    device.startActivity(component=runComponent)
    #device.startActivity(component='com.douban.movie/com.douban.movie.app.HomeActivity')
    return device

def addSnapShot():
    results.append(device.takeSnapshot())

def touchPoint(x,y):
    device.touch(x,y,MonkeyDevice.DOWN_AND_UP)
    addSnapShot()

def backWithCode():
    device.press('KEYCODE_BACK',MonkeyDevice.DOWN_AND_UP)

def backWithPoint():
    device.touch(small/15,big/30,MonkeyDevice.DOWN_AND_UP)

#水平点击当前行的所有元素
def touchHorizontal(y):
    addSnapShot()
    mainSnap = results[-1]
    for x in range(beginX,small,incX):
        if isMainActivity(mainSnap, results[-1]):
            touchPoint(x,y)
            MonkeyRunner.sleep(1.0)
            #slideDown()
            if not isMainActivity(mainSnap, results[-1]):
                addSnapShot()
                backWithCode()
            MonkeyRunner.sleep(0.5)


def touchAllOnScreen():
    global beginY
    for i in range(8):
        touchHorizontal(beginY)
        slideDown(270)

def isMainActivity(snap,mainSnap):
    return snap.sameAs(mainSnap,0.8)

def slideDown(length):
    device.drag((small/2,big/5+length),(small/2,big/5),1,100)

def slideUp():
    device.drag((small/2,big/5),(small/2,big/5*4),1,100)

def slideRight():
    device.drag((small/10*9,big/2),(small/10,big/2),1,100)

def slideLeft():
    device.drag((small/10,big/2),(small/10*9,big/2),1,100)

def savePng():
    results[0].writeToFile('snapshot/douban/capture0.png','png')
    results[1].writeToFile('snapshot/douban/capture1.png','png')
    for i in range(2,len(results)):
        cur = results[i]
        prev = results[i-1]
        pprev = results[i-2]
        if(cur.sameAs(prev,0.8) or cur.sameAs(pprev,0.8)):
            continue
        else:
            cur.writeToFile('snapshot/douban/capture%d.png'%i,'png')

def main():
    global device,big,small,incX,incY,beginX,beginY,results

    device = deviceInit()
    print('Initializing device and starting main activity...')
    MonkeyRunner.sleep(6.0)

    big = int(device.getProperty('display.width'))#模拟器的width是较大的那个数
    small = int(device.getProperty('display.height'))#height是较小的那个数
    
    incX = 180
    incY = 100
    beginX = 90
    beginY = 128
    results = []

    print('Current scrreen traversal...')
    touchAllOnScreen()
    print('Filtering snapshot and saving...')
    savePng()

if __name__ == '__main__':
    #main()
    print(argv[1])
    print(argv[2])