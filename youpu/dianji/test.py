#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import threading
import queue

q = queue.Queue()


def producer(arg):
    """
    生产者
    :param arg:
    :return:
    """
    while True:
        time.sleep(2)
        print("厨师生产包子%s号" % arg)
        q.put(arg)


for i in range(1, 4):
    t = threading.Thread(target=producer, args=(i,))
    t.start()


def consumer(arg):
    """
    消费者
    :param arg:
    :return:
    """
    while True:
        time.sleep(1)
        q.get(arg)
        print("消费者吃包子")


for i in range(5):
    print("i"+str(i))
    t = threading.Thread(target=consumer, args=(i,))
    t.start()