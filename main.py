import sys
import time
import os
import pyautogui
from pynput import keyboard
import tkinter as tk
import threading
import pygetwindow as gw

pgup = keyboard.Key.page_up
pgdn = keyboard.Key.page_down
esc = keyboard.Key.delete

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from pyautogui import *
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR, draw_ocr


class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)


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
        image = screenshot(region=POSITIONS["againtext"])  # 使用pyautogui进行截图操作
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


def nopower(path="", printResult=False):
    image = screenshot(region=POSITIONS["fulfill"])  # 使用pyautogui进行截图操作
    image = np.array(image)

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
                if "开拓力补充" in text:
                    return True
                else:
                    return False


def start():
    windows = gw.getWindowsWithTitle("崩坏：星穹铁道")
    if windows:  # 如果找到了窗口
        windows[0].activate()  # 激活第一个窗口
    else:
        print("未找到窗口")
        print_to_gui("未找到窗口,请手动打开游戏")
        return
    time.sleep(1)
    while True:
        if text_in_screen(printResult=True):
            print("Success")
            print_to_gui("找到目标，再来一遍")
            pyautogui.moveTo(*POSITIONS["again"])
            pyautogui.click()
            time.sleep(1)
        else:
            if nopower(printResult=True):
                print("No power")
                print_to_gui("体力不足，程序已停止")
                stop_thread(None)
            print("not found")
            print_to_gui("未找到目标")
            time.sleep(10)


def print_to_gui(message, emphasis=False):
    timestamp = get_curtime()
    message_with_timestamp = f"{timestamp}: {message}\n"
    if emphasis:
        tag = "emphasis"
    else:
        tag = "blue"
    text.insert(tk.END, message_with_timestamp, tag)
    text.see(tk.END)


def on_press(key):
    if key == pgup:
        start_thread(None)
    elif key == pgdn:
        stop_thread(None)
    elif key == esc:
        root.destroy()
        sys.exit()


def start_thread(event):
    global thread
    thread = threading.Thread(target=start)
    thread.daemon = True
    thread.start()
    print_to_gui("The program has started!", emphasis=True)


def stop_thread(event):
    if thread.is_alive():
        # Terminate the thread
        # Note: This is generally not recommended, but we don't have other options here
        # as Python doesn't support killing threads directly.
        import ctypes
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
        print_to_gui("The program has stopped!", emphasis=True)


POSITIONS = {
    "auto": (1762, 46),
    "againtext": (1200, 910, 110, 60),
    "again": (1200, 930),
    "fulfill": (870, 320, 200, 50),
    # 添加更多坐标...
}

if __name__ == '__main__':
    root = tk.Tk()
    screen_height = root.winfo_screenheight()  # 获取屏幕高度
    window_height = 150  # 窗口高度
    y = (screen_height - window_height) // 2  # 计算y坐标
    root.geometry(f'400x{window_height}+0+{y}')  # 设置窗口大小和位置
    root.attributes('-alpha', 0.8)  # 设置透明度为80%
    root.attributes('-topmost', True)
    root.overrideredirect(True)  # 创建无边框窗口
    # 添加一个按钮
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    text = tk.Text(root)
    text.pack()

    text.tag_configure("red", foreground="red", font=("Helvetica", 12))
    text.tag_configure("blue", foreground="blue", font=("Helvetica", 12))
    text.tag_configure("emphasis", foreground="red", font=("Helvetica", 15), underline=True)

    root.mainloop()
