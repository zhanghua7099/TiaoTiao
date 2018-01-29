import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time
import random


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


def getPeople(pivot, screen, range=0.3, num=10):
    '''基于多尺度搜索'''
    H, W = screen.shape[:2]
    h, w = pivot.shape[:2]

    found = None
    for scale in np.linspace(1-range, 1+range, num)[::-1]:
        resized = cv2.resize(screen, (int(W * scale), int(H * scale)))
        r = W / float(resized.shape[1])
        if resized.shape[0] < h or resized.shape[1] < w:
            break
        res = cv2.matchTemplate(resized, pivot, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= res.max())
        pos_h, pos_w = list(zip(*loc))[0]

        if found is None or res.max() > found[-1]:
            found = (pos_h, pos_w, r, res.max())

    if found is None: return (0,0,0,0,0)
    pos_h, pos_w, r, score = found
    start_h, start_w = int(pos_h * r), int(pos_w * r)
    end_h, end_w = int((pos_h + h) * r), int((pos_w + w) * r)
    x = (end_w - start_w)/2+start_w
    y = (end_h-start_h)/2+start_h
    return x, y


coordinate = []
player = cv2.imread("./player.png")
def on_press(event):
    global coordinate
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
    x1, y1 = coordinate[0], coordinate[1]
    img = cv2.imread('./Screen/screenshot.png')
    x2, y2 = getPeople(player, img)
    s = math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))
    time1 = int(s*1.45)
    jump(random.randint(700, 750), time1)
    coordinate = []
    time.sleep(1)
