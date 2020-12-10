# coding: utf-8

from common.handleDB import HandleMysql
from common.readconfig import ReadConfig
from open_chrome import oneThread
import time
import requests
import json
from selenium import webdriver  # 浏览器驱动器
import random


class Myspider:
    def __init__(self):
        self.handleMysql = HandleMysql()
        self.readConfig = ReadConfig()

    def get_config(self, sql):
        return self.handleMysql.fetch_db(sql)

    def get_window_size(self):
        return self.readConfig.get_window_size()


if __name__ == '__main__':
    myspider = Myspider()  # 读取配置文件
    window_size = myspider.get_window_size().split(",")
    for i in range(3):
        time.sleep(1)
        sql = "select * from ua order by rand() limit 10"
        ua = []
        for i in myspider.get_config(sql):
            ua.append(i)

        request = requests.get(
            "http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=88d304d14273946c00cd3cabc7d25199&orderNo=GL20201208142456Pe5sEDu6&count=10&isTxt=0&proxyType=1")
        ip_port = json.loads(request.text)
        words = ["400电话代理", "400电话代理"]
        site = "www.4006.com"
        # 新建线程，每个线程单独使用一个尺寸，UA，和IP PORT
        for i in range(10):
            # rand = random.randint(0, ip_port['obj'].__len__() - 1)
            port = ip_port['obj'][i - 1]['port']
            ip = ip_port['obj'][i - 1]['ip']
            # options = webdriver.ChromeOptions()  # 设置代理
            # options.add_argument("--proxy-server=http://" + ip + ":" + port)
            # options.add_argument('lang=zh_CN.UTF-8')
            # options.add_argument('user-agent="' + ua[random.randint(0, ua.__len__() - 1)][0] + '"')
            # driver = webdriver.Chrome(options=options)
            # driver.set_window_size(window_size[random.randint(0, window_size.__len__() - 1)].split("*")[0], window_size[random.randint(0, window_size.__len__() - 1)].split("*")[1])  # 分辨率 1024*768
            # one = oneThread(words, site, driver)
            one = oneThread(words, site, "--proxy-server=http://" + ip + ":" + port,
                            'user-agent="' + ua[random.randint(0, ua.__len__() - 1)][0] + '"',
                            window_size[random.randint(0, window_size.__len__() - 1)].split("*")[0],
                            window_size[random.randint(0, window_size.__len__() - 1)].split("*")[1])
            one.start()
            time.sleep(0.5)
