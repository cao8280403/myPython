#!/usr/bin/env python
# coding=utf-8
import threading
import json

from aliip import Aliip


class Dianji_thread(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        # 初始化的时候 需要获取ip and port 设置ua 使用传递过来的参数ua
        obj_aliip = Aliip()
        self.res = json.loads(obj_aliip.requesturl(self.ip))
        # city = msg["City"]
        # county = msg["County"]

    def getResult(self):
        return self.res