#!/usr/bin/python3

from selenium import webdriver  # 浏览器驱动器
from selenium.webdriver.common.by import By  # 定位器
from selenium.webdriver.common.keys import Keys  # 键盘对象
from selenium.webdriver.support import expected_conditions as EC  # 判断器
from selenium.webdriver.support.wait import WebDriverWait  # 浏览器等待对像
import time
import json
import win32api
import random
from selenium.webdriver.common.action_chains import ActionChains
import threading


class myThread(threading.Thread):
    def __init__(self, words):
        threading.Thread.__init__(self)
        self.words = words

    def run(self):
        print("begin thread：")
        # print_time(self.name, self.counter, 5)
        random_count = self.one_circle(self.words[0], "1")

        if random_count == 1:
            self.one_circle(self.words[1], "2")
            print("two circle over")
        else:
            print("only one circle over")
        # 修改关键词后再次执行方法one_circle
        print("end thread：")

    def one_circle(self, word, count):
        print("begin circle：word is " + word + " count is " + count)


        self.normal_step(word)
        # 最后的走向判断
        if count == "2":
            return 2
        else:
            # 随机返回一个值
            random_count = random.randint(0, 1)
            if random_count == 1:
                print("return ")
                return 1
            else:
                print("go on")


    def normal_step(self, word):
        print("normal_step")



def main():
    print("start __main__")
    words = ["400电话", "400电话办理"]
    thread1 = myThread(words)
    thread1.start()
    print("end __main__")


if __name__ == '__main__':
    main()
