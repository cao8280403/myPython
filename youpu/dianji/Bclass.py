#!/usr/bin/env python
# coding=utf-8
import threading
import json
from db_class import Updatedb


class Bclass(object):
    total_ids = []

    def __init__(self):
        self.name = ''

    def add(self, oneid):
        # 把成功的id添加进去，完事儿后判断是否满足1000个，满足了就提交到数据库
        self.total_ids.append(oneid)
        if len(self.total_ids) >= 10:
            aaa = self.total_ids
            for i in aaa:
                print(i)
            self.total_ids = []
            # updatedb = Updatedb()
            # updatedb.updatedb(aaa)



