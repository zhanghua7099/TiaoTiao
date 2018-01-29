import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time
import random
from PIL import Image


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


def find_piece_and_board(im):
    """
    寻找关键坐标
    """
    w, h = im.size

    piece_x_sum = 0
    piece_x_c = 0
    piece_y_max = 0
    board_x = 0
    board_y = 0
    scan_x_border = int(w / 8)  
    scan_start_y = 0  
    im_pixel = im.load()
    for i in range(int(h / 3), int(h*2 / 3), 50):
        last_pixel = im_pixel[0, i]
        for j in range(1, w):
            pixel = im_pixel[j, i]
            if pixel != last_pixel:
                scan_start_y = i - 50
                break
        if scan_start_y:
            break
    print('scan_start_y: {}'.format(scan_start_y))
    for i in range(scan_start_y, int(h * 2 / 3)):
        for j in range(scan_x_border, w - scan_x_border):
            pixel = im_pixel[j, i]
            if (50 < pixel[0] < 60) \
                    and (53 < pixel[1] < 63) \
                    and (95 < pixel[2] < 110):
                piece_x_sum += j
                piece_x_c += 1
                piece_y_max = max(i, piece_y_max)

    if not all((piece_x_sum, piece_x_c)):
        return 0, 0, 0, 0
    piece_x = int(piece_x_sum / piece_x_c)
    piece_y = piece_y_max - 20  
    if piece_x < w/2:
        board_x_start = piece_x
        board_x_end = w
    else:
        board_x_start = 0
        board_x_end = piece_x

    for i in range(int(h / 3), int(h * 2 / 3)):
        last_pixel = im_pixel[0, i]
        if board_x or board_y:
            break
        board_x_sum = 0
        board_x_c = 0

        for j in range(int(board_x_start), int(board_x_end)):
            pixel = im_pixel[j, i]
            if abs(j - piece_x) < 20:
                continue
            if abs(pixel[0] - last_pixel[0]) \
                    + abs(pixel[1] - last_pixel[1]) \
                    + abs(pixel[2] - last_pixel[2]) > 10:
                board_x_sum += j
                board_x_c += 1
        if board_x_sum:
            board_x = board_x_sum / board_x_c
    last_pixel = im_pixel[board_x, i]
    for k in range(i+274, i, -1):  
        pixel = im_pixel[board_x, k]
        if abs(pixel[0] - last_pixel[0]) \
                + abs(pixel[1] - last_pixel[1]) \
                + abs(pixel[2] - last_pixel[2]) < 10:
            break
    board_y = int((i+k) / 2)
    for j in range(i, i+200):
        pixel = im_pixel[board_x, j]
        if abs(pixel[0] - 245) + abs(pixel[1] - 245) + abs(pixel[2] - 245) == 0:
            board_y = j + 10
            break

    if not all((board_x, board_y)):
        return 0, 0, 0, 0
    return piece_x, piece_y, board_x, board_y


while True:
    getScreen()
    im = Image.open('./Screen/screenshot.png')
    x2, y2, x1, y1 = find_piece_and_board(im)
    s = math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))
    time1 = int(s*1.39)
    jump(random.randint(700, 750), time1)
    time.sleep(1)
