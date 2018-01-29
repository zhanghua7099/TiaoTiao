import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time
import random


coordinate = []


def getScreen():
    '''获取手机屏幕图片并保存至Screen文件下'''
    ScreenShot = 'adb shell /system/bin/screencap -p /sdcard/screenshot.png'
    ScreenSave = 'adb pull /sdcard/screenshot.png ./Screen'
    os.system(ScreenShot)
    os.system(ScreenSave)


def jump(x, time):
    '''在手机屏幕坐标（x,x）处按压time（ms）'''
    parameter = str(x)+' '+str(x)+' '+str(x)+' '+str(x)+' '+str(time)
    jumpCommand = 'adb shell input swipe '+parameter
    os.system(jumpCommand)


def on_press(event):
    global coordinate
    if len(coordinate) == 0:
        coordinate.append(event.xdata)
        coordinate.append(event.ydata)
    elif len(coordinate) == 2:
        coordinate.append(event.xdata)
        coordinate.append(event.ydata)
        plt.close()



while True:
    getScreen()
    img = cv2.imread('./Screen/screenshot.png', 0)
    fig = plt.figure()
    plt.imshow(img, animated= True)
    fig.canvas.mpl_connect('button_press_event', on_press)
    plt.show()
    if len(coordinate) != 0:
        x1, y1 = coordinate[0], coordinate[1]
        x2, y2 = coordinate[2], coordinate[3]
        s = math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        time1 = int(s*1.36)
        jump(random.randint(700, 750), time1)
    coordinate = []
    time.sleep(1)
