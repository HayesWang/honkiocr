import time

import numpy
import os

import pyautogui

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from pyautogui import *
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR, draw_ocr




class Region:
    again = (1200, 910, 1310, 970)
def get_curtime(time_format="%Y-%m-%d %H:%M:%S"):
    curTime = time.localtime()
    curTime = time.strftime(time_format, curTime)
    return curTime


def text_in_screen(path="", printResult=False):
    '''
    图像文字识别
    :param path:图片路径
    :param printResult:是否打印出识别结果
    :return:result,img_name
    '''
    image = path

    # 图片路径为空就默认获取屏幕截图
    if image == "":
        image = screenshot(region=(1200, 910, 110, 60))  # 使用pyautogui进行截图操作
        image = np.array(image)
    else:
        # 不为空就打开
        image = Image.open(image).convert('RGB')

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

    result = ocr.ocr(image, cls=True)
    if result is None:
        return False

    if printResult is True:
        for line in result:
            if line is None:
                continue
            for word in line:
                if word is None:
                    continue
                text = word[1][0]
                if "再来一次" in text:
                    return True
                else:
                    return False

if __name__ == '__main__':
    time.sleep(2)
    while True:
        if text_in_screen(printResult=True):
            print("Success")
            pyautogui.moveTo(1240,930, duration=0.25)
            pyautogui.click()
            time.sleep(1)
        else:
            time.sleep(20)
            print("not found")