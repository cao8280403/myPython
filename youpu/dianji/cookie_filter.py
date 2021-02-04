#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column, String, create_engine, ForeignKey, func
from fetchip import Fetchip
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from db_class import Mipcms_fabao_history, Mipcms_fabao, City_cookies, Mipcms_fabao_list, Mipcms_fabao_server_record, \
    Mipcms_fabao_server_switch, Mipcms_ip, Backup_cookies
from aliip import Aliip
from dianji_thread import Dianji_thread
import os
import platform
import ctypes
import requests
import threading
from selenium import webdriver  # 浏览器驱动器
from selenium.webdriver.common.by import By  # 定位器
from selenium.webdriver.common.keys import Keys  # 键盘对象
from selenium.webdriver.support import expected_conditions as EC  # 判断器
from selenium.webdriver.support.wait import WebDriverWait  # 浏览器等待对像
from selenium.webdriver.chrome.service import Service
import time, pyautogui
import json
import os
import random
from selenium.webdriver.common.action_chains import ActionChains
import threading
from aliip import Aliip
from Bclass import Bclass
import psutil
import traceback
import win32api, win32con
from readconfig import ReadConfig

gids = []
delete_cookies = []
update_cookies = []
success_count = 0
httpIP = 0
not_exist_zone = []
loop_now_time = time.time() - 1
submit_time = time.time() - 1
loop_jiange_time = 38
submit_jiange_time = 0
all_ips = []
last_cookie_id = 0


class oneThread(threading.Thread):
    # def __init__(self, word_one, word_two, site, arg1, ip, citycookies, show_window, proxies, n, arg_x, ip_min):
    def __init__(self, arg1, cookie, show_window, ua):
        threading.Thread.__init__(self)
        self.arg1 = arg1
        self.cookie = cookie
        self.show_window = show_window
        self.ua = ua

    def run(self):
        global delete_cookies
        try:
            # 初始化的时候 需要获取ip and port 设置ua 使用传递过来的参数ua
            options = webdriver.ChromeOptions()  # 设置代理
            options.add_argument(self.arg1)
            options.add_argument('lang=zh_CN.UTF-8')
            options.add_argument('--disk-cache-dir=d:\chromecahce')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹
            if self.show_window == 'no':
                options.headless = True
            options.add_argument('log-level=3')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示正在受自动化软件控制#跟上面只能选一个
            options.add_argument('user-agent="' + self.ua + '"')
            options.add_argument('Connection="close"')
            driver = webdriver.Chrome(options=options)
            try:
                driver.get("https://www.baidu.com")
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="su"]'))
                )
                driver.delete_all_cookies()
                cookie_list_array = self.cookie.cookie.split(";")
                for tmp_cookie in cookie_list_array:
                    cookie_dict = {
                        "domain": ".baidu.com",  # 火狐浏览器不用填写，谷歌要需要
                        'name': tmp_cookie.split("=")[0],
                        'value': tmp_cookie.split("=")[1],
                        "expires": "",
                        'path': '/',
                        'httpOnly': False,
                        'HostOnly': False,
                        'Secure': False}
                    driver.add_cookie(cookie_dict)
                driver.refresh()

                time.sleep(random.randint(2, 3))

                # 判断是否登录，右上角是否存在那个登录按钮
                usernames = driver.find_elements_by_class_name("user-name")
                if len(usernames) == 0:
                    delete_cookies.append(self.cookie)
                driver.quit()
            except Exception as error:
                if 'Connection aborted' in str(error):
                    delete_cookies.append(self.cookie)
                driver.quit()
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " error main process: " + str(error))
        except Exception as error:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 2: " + str(error))


class Aclass(object):
    def __init__(self):
        self.cookies = []
        self.uas = []

    def fetch_thousand_cookies(self):
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        # all_count = session.query(func.count(Backup_cookies.id)).scalar()
        cookies = session.query(Backup_cookies).filter(Backup_cookies.id >= last_cookie_id).limit(1000).all()
        print(len(cookies))
        self.cookies = cookies

    def fetch_ua(self):
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        uas = session.query(City_cookies.ua).all()
        print(len(uas))
        self.uas = uas


if __name__ == '__main__':
    print("begin process")
    try:
        aliip = Aliip()

        readConfig = ReadConfig()
        num = readConfig.get_url()
        prams = readConfig.get_pram()
        get_window_size = readConfig.get_window_size()
        ip_min = prams[0]
        show_window = prams[1]
        open_chrome_sec = prams[2]
        pool_num = prams[3]
        server_id = prams[4]
        ip_address = prams[5]
        sizelist = get_window_size.split(",")
        aclass = Aclass()
        try:
            aclass.fetch_ua()
        except Exception as err:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + str(err))
            time.sleep(60)
        loop_count = 0
        while True:

            try:
                # 判断是否有需要删除的
                if len(delete_cookies) > 0:
                    bbb = []
                    for tmp in delete_cookies:
                        if tmp != '':
                            bbb.append(tmp.id)
                    ccc = tuple(bbb)
                    engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
                    # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()  # 创建session
                    delete_count = session.query(Backup_cookies).filter(Backup_cookies.id.in_(ccc)).delete(
                        synchronize_session=False)
                    session.commit()
                    delete_cookies = []
                    session.close()
                if len(aclass.cookies) > 0:
                    obj_fetchip = Fetchip(num, ip_min)
                    ips = obj_fetchip.requesturl()
                    # 这批ip使用10次
                    for n in range(int(pool_num)):
                        threads = []
                        for ip in ips:
                            cookie = aclass.cookies.pop(0)
                            one = oneThread("--proxy-server=http://" + ip["ip"] + ":" + ip["port"],
                                            cookie, show_window, aclass.uas[random.randint(0, len(aclass.uas) - 1)].ua)
                            threads.append(one)
                        for thread in threads:
                            time.sleep(int(open_chrome_sec))
                            thread.start()
                        print("threads")
                else:
                    # 取新的一批cookie
                    aclass.fetch_thousand_cookies()
                    if len((aclass.cookies)) == 0:
                        break
                    last_cookie_id = aclass.cookies[len((aclass.cookies)) - 1].id+1

            except Exception as err:
                print(time.strftime("%Y-%m-%d %H:%M:%S") + "error 9: " + str(err))
                time.sleep(10)

    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 4: " + str(err))
print("end process")
