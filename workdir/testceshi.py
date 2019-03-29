#!/usr/bin/python
# -*- coding:utf-8 -*-

from selenium import webdriver

import time

# driver = webdriver.Firefox()  # 初始化一个火狐浏览器实例：driver
driver = webdriver.Chrome()  # 初始化一个火狐浏览器实例：driver

driver.maximize_window()  # 最大化浏览器

time.sleep(5)  # 暂停5秒钟

driver.get("http://120.79.117.64:3003/sub1/key1")  # 通过get()方法，打开一个url站点
print(driver.page_source)
driver.close()