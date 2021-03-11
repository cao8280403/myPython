#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column, String, create_engine, ForeignKey, func
from fetchip import Fetchip
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from db_class import Mipcms_fabao_history, Mipcms_fabao, City_cookies, Mipcms_fabao_list, Mipcms_fabao_server_record, \
    Mipcms_fabao_server_switch, Mipcms_ip,Cookie_list,Cookie_list
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
memCpu = ''
end_word = ['推荐', '排名', '推荐', '排名', '价格', '价格', '价格', '价格', '价格', '价格', '价格', '厂家', '厂家', '厂家', '厂家', '厂家', '厂家', '厂家',
            '公司', '公司', '公司', '公司', '公司', '公司', '公司', '公司', '公司', '电话', '服务', '方案', '服务', '方案', '服务', '方案', '电话', '教程',
            '电话', '教程', '电话', '教程', '电话', '教程', '电话', '教程', '费用', '费用', '费用', '说明', '策划', '素材', '案例', '合同', '合同', '合同',
            '合同', '套餐', '模板', '论坛', '知识', '一条龙', '专家', '协议', '网', '网', '网', '网', '网', '2020', '2021', '哪家好', '哪家好',
            '哪家好', '哪家好', '哪家强', '怎么办', '怎么办', '怎么办', '怎么弄', '怎么搞', '多少钱', '是什么', '如何办', '吗', '呀']


class oneThread(threading.Thread):
    # def __init__(self, word_one, word_two, site, arg1, ip, citycookies, show_window, proxies, n, arg_x, ip_min):
    def __init__(self, word_one, site, arg1, ip, city, county, cookie, show_window, proxies, n, arg_x, ip_min,
                 total_loop_count, use_cookie, cities,first_word,ua):
        threading.Thread.__init__(self)
        self.word_one = word_one
        # if word_two != "":
        #     self.word_two = word_two
        # else:
        #     self.word_two = ""
        self.site = site
        self.arg1 = arg1
        self.ip = ip
        self.city = city
        self.county = county
        self.cookie = cookie
        self.show_window = show_window
        self.proxies = proxies
        self.sleep_time = n
        self.arg_x = arg_x
        self.ip_min = ip_min
        self.total_loop_count = total_loop_count
        self.use_cookie = use_cookie
        self.cities = cities
        self.first_word = first_word
        self.ua = ua

    def run(self):
        global delete_cookies
        global update_cookies
        global httpIP
        global not_exist_zone
        global memCpu
        global end_word
        word = self.word_one
        if self.sleep_time == self.total_loop_count - 1:
            memCpu = getMemCpu()
        try:
            # 初始化的时候 需要获取ip and port 设置ua 使用传递过来的参数ua
            # print("begin thread：")
            options = webdriver.ChromeOptions()  # 设置代理
            options.add_argument(self.arg1)
            options.add_argument('lang=zh_CN.UTF-8')
            # options.add_argument('--disk-cache-dir=d:\chromecahce')
            # prefs = {"profile.managed_default_content_settings.images": 2}
            # options.add_experimental_option("prefs", prefs)
            # options.add_argument('--host-resolver-rules=MAP ' + self.site + ' 127.0.0.1')
            # options.add_argument("--disable-gpu")  # 禁用gpu
            # options.add_argument("disable-cache")  # 禁用缓存
            # options.add_argument('--disable-application-cache')
            # options.add_argument('--incognito')  # 隐身模式（无痕模式）
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹
            # options.add_argument('--ignore-certificate-errors')
            # options.add_argument('--disable-infobars')  # 不显示正在受自动化软件控制  失效
            if self.show_window == 'no':
                options.headless = True
            options.add_argument('log-level=3')
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
            options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示正在受自动化软件控制#跟上面只能选一个
            # # 根据ip获取阿里ip的地域
            # aliip = Aliip()
            # ali_result = aliip.requesturl(self.ip)
            # json_result = json.loads(ali_result)
            cookie_list_str = ''
            tmp_city_cookie = ''
            ua = ""
            if not use_cookie == "yes":
                ua = self.ua
            else:
                ua = self.cookie[0]["ua"]

            options.add_argument('user-agent="' + ua + '"')
            options.add_argument('Connection="close"')
            driver = webdriver.Chrome(options=options)
            try:
                httpIP = httpIP + 1
                driver.maximize_window()
                driver.get("https://www.baidu.com")
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="su"]'))
                )
                if self.use_cookie == 'yes':
                    if cookie_list_str != '':
                        driver.delete_all_cookies()
                        cookie_list_array = cookie_list_str.split(";")
                        for tmp_cookie in cookie_list_array:
                            cookie_dict = {
                                "domain": ".baidu.com",  # 火狐浏览器不用填写，谷歌要需要
                                'name': tmp_cookie.split("=")[0].strip(),
                                'value': tmp_cookie.split("=")[1].strip(),
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
                        delete_cookies.append(tmp_city_cookie)
                time.sleep(random.randint(1, 2))
                # 去掉城市名
                change_keyword = str(self.first_word)
                for tmp_city in self.cities:
                    if str(tmp_city[0]) in change_keyword:
                        change_keyword = change_keyword.replace(tmp_city[0], "").replace("市", "")

                # if change_keyword.__len__() > 3:
                #     change_keyword = change_keyword[0:-2]
                if random.randint(1, 100)>95:
                    change_keyword = change_keyword + self.city
                if random.randint(1, 100) > 95:
                    change_keyword = change_keyword + end_word[random.randint(0, end_word.__len__()-1)]

                uri = "https://www.baidu.com/s?ie=UTF-8&wd=" + change_keyword + "&f=8&si=" + self.site + "&ct=2097152"
                driver.get(uri)

                wait = WebDriverWait(driver, 8, 1)
                # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
                wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))

                time.sleep(random.randint(1, 3))
                # 滚动下
                js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(random.randint(2, 6))
                driver.execute_script(js)

                if random.randint(1,5)==5:
                    tops = driver.find_elements_by_xpath("//div[@class='cr-content  new-pmd']//tr[@class='toplist1-tr']")
                    if tops.__len__()>0:
                        top = tops[random.randint(0,9)]
                        driver.execute_script("arguments[0].scrollIntoView();", top)
                        # 再向上移动200
                        js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                        driver.execute_script(js)
                        a = top.find_elements_by_xpath(".//a")[0]
                        ActionChains(driver).click(a).perform()
                        windows = driver.window_handles
                        driver.switch_to.window(windows[-1])
                        now_height = random.randint(2, 6)
                        js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                        driver.execute_script(js)
                        time.sleep(random.randint(1, 3))
                        # 执行1-5次的滚动（50%上滚、50%下滚），幅度为随机20%~60%的高度，每次滚动后停留随机1~3秒
                        for i in range(random.randint(1, 3)):
                            if random.randint(1, 2) == 1:
                                now_height = min(now_height + random.randint(1, 5), 10)
                                if now_height == 0:
                                    js = "document.documentElement.scrollTop=document.body.scrollTop"
                                else:
                                    js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(
                                        now_height)
                                driver.execute_script(js)
                                time.sleep(random.randint(1, 3))
                            else:
                                tmp = random.randint(1, 5)
                                now_height = now_height - tmp if now_height > tmp else 0
                                if now_height == 0:
                                    js = "document.documentElement.scrollTop=document.body.scrollTop"
                                else:
                                    js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(
                                        now_height)
                                driver.execute_script(js)
                                time.sleep(random.randint(1, 3))
                        driver.close()
                        windows = driver.window_handles
                        driver.switch_to.window(windows[0])




                time.sleep(1)
                inputs = driver.find_element_by_id("kw")
                ActionChains(driver).click(inputs).perform()
                for i in range(15):
                    inputs.send_keys(Keys.BACKSPACE)
                    time.sleep(random.randint(1, 2) / 10)
                for keyword in word["keyword"]:
                    inputs.send_keys(keyword)
                    random_count = random.randint(1, 10)
                    time.sleep(random_count / 10)
                su = driver.find_element_by_id("su")
                ActionChains(driver).click(su).perform()
                wait = WebDriverWait(driver, 3, 1)
                # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
                wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
                time.sleep(random.randint(2, 3))

                # 判断是否存在广告，先点广告
                ads = driver.find_elements_by_xpath("//div[@data-ecimtimesign]")
                if ads.__len__() > 0:
                    random_index = random.randint(0, ads.__len__() - 1)
                    dest = ads[random_index]
                    driver.execute_script("arguments[0].scrollIntoView();", dest)
                    # 再向上移动200
                    js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                    driver.execute_script(js)
                    a = dest.find_element_by_xpath(".//a[1]")
                    ActionChains(driver).click(a).perform()
                    time.sleep(random.randint(1, 3))
                    windows = driver.window_handles
                    driver.switch_to.window(windows[-1])
                    driver.close()
                    driver.switch_to.window(windows[0])
                    time.sleep(random.randint(1, 3))
                # else:
                #     js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(random.randint(2, 6))
                #     driver.execute_script(js)
                #     time.sleep(1)
                #     driver.quit()

                try:
                    proxies = {'http': self.proxies}
                    # 恶意访问将ip拉入黑名单
                    for t in range(7):
                        time.sleep(0.1)
                        r = requests.get("http://" + self.site + "/shell.php", proxies=proxies, timeout=3)
                        r = requests.get("http://zhouhangxinnengyuan.com/", proxies=proxies, timeout=3)
                except Exception as error:
                    print("error attack: " + str(error))

                now_height = random.randint(2, 6)
                js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                driver.execute_script(js)
                time.sleep(random.randint(1, 3))
                # 执行1-5次的滚动（50%上滚、50%下滚），幅度为随机20%~60%的高度，每次滚动后停留随机1~3秒
                for i in range(random.randint(1, 3)):
                    if random.randint(1, 2) == 1:
                        now_height = min(now_height + random.randint(1, 5), 10)
                        if now_height == 0:
                            js = "document.documentElement.scrollTop=document.body.scrollTop"
                        else:
                            js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                        driver.execute_script(js)
                        time.sleep(random.randint(1, 3))
                    else:
                        tmp = random.randint(1, 5)
                        now_height = now_height - tmp if now_height > tmp else 0
                        if now_height == 0:
                            js = "document.documentElement.scrollTop=document.body.scrollTop"
                        else:
                            js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                        driver.execute_script(js)
                        time.sleep(random.randint(1, 3))
                if not (word["short_title"]) is None and len(word["short_title"]) > 0:
                    # 判断
                    # 如果标题不包括带的标题
                    # 获取所有标题
                    divs = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
                    tmp_index = 100
                    for div in divs:
                        tmp_title = div.find_element_by_xpath(".//a[1]").text
                        if str(word["short_title"]) in tmp_title:
                            tmp_index = divs.index(div)
                            break
                    if tmp_index < 100:
                        dest = divs[tmp_index]
                        driver.execute_script("arguments[0].scrollIntoView();", dest)
                        # 再向上移动200
                        js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                        driver.execute_script(js)
                        time.sleep(random.randint(2, 3))
                        a = dest.find_element_by_xpath(".//a[1]")
                        ActionChains(driver).click(a).perform()
                        windows = driver.window_handles
                        driver.switch_to.window(windows[-1])
                        self.last_step(word, driver)
                    else:
                        #判断是否有首页，有则点击
                        dict35 = {}
                        divs35 = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
                        for div in divs35:
                            divas = div.find_elements_by_xpath(".//div//a")
                            for diva in divas:
                                if diva.text == self.site + "/":
                                    tmp = divs35.index(div)
                                    dict35[tmp] = diva.text
                        if dict35.__len__() > 0:
                            index = sorted(dict35.items())[0][0]
                            dest = divs35[index]
                            driver.execute_script("arguments[0].scrollIntoView();", dest)
                            # 再向上移动200
                            js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                            driver.execute_script(js)
                            time.sleep(random.randint(3, 5))

                            miaoshu = dest.find_element_by_xpath(".//div[@class='c-abstract']")
                            ActionChains(driver).click(miaoshu).perform()
                            time.sleep(random.randint(3, 5))

                            random_num = random.randint(1, 100)

                            if random.randint(1, 5) == 5:
                                # 标题
                                if random_num > 20:
                                    index = sorted(dict35.items())[0][0]
                                    dest = divs35[index]
                                    a = dest.find_element_by_xpath(".//a[1]")
                                    ActionChains(driver).click(a).perform()
                                    windows = driver.window_handles
                                    driver.switch_to.window(windows[-1])
                                    self.last_step(word, driver)
                                # 网址
                                elif random_num < 6:
                                    index = sorted(dict35.items())[0][0]
                                    dest = divs35[index]
                                    node_div = dest.find_elements_by_xpath("./div")
                                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                    if node_div.__len__() == 1:
                                        a = dest.find_element_by_xpath("./div[1]/div[2]/div[2]/a[1]")
                                        ActionChains(driver).click(a).perform()
                                        windows = driver.window_handles
                                        driver.switch_to.window(windows[-1])
                                        self.last_step(word, driver)
                                    else:
                                        a = dest.find_element_by_xpath("./div[2]/a[1]")
                                        # ActionChains(driver).move_to_element(a).perform()
                                        # time.sleep(300)
                                        ActionChains(driver).click(a).perform()
                                        windows = driver.window_handles
                                        driver.switch_to.window(windows[-1])
                                        self.last_step(word, driver)
                                # 图片
                                else:
                                    index = sorted(dict35.items())[0][0]
                                    dest = divs35[index]
                                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                    node_div = dest.find_elements_by_xpath("./div")
                                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                    if node_div.__len__() == 1:
                                        a = dest.find_element_by_xpath("./div[1]/div[1]/a[1]")
                                        ActionChains(driver).click(a).perform()
                                        windows = driver.window_handles
                                        driver.switch_to.window(windows[-1])
                                        self.last_step(word, driver)
                        else:
                            # driver.quit()
                            dest = divs[0]
                            driver.execute_script("arguments[0].scrollIntoView();", dest)
                            # 再向上移动200
                            js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                            driver.execute_script(js)
                            time.sleep(random.randint(2, 3))
                            a = dest.find_element_by_xpath(".//a[1]")
                            ActionChains(driver).click(a).perform()
                            windows = driver.window_handles
                            driver.switch_to.window(windows[-1])
                            self.last_step(word, driver)

                        # driver.get(
                        #     "https://www.baidu.com/s?ie=UTF-8&wd=" + word[
                        #         "keyword"] + "&rn=2&si=" + self.site + "&ct=2097152")
                        # # time.sleep(random.randint(2, 3))
                        # # su = driver.find_element_by_id("su")
                        # # ActionChains(driver).click(su).perform()
                        # # wait = WebDriverWait(driver, 3, 1)
                        # # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
                        # # wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
                        # time.sleep(random.randint(2, 3))
                        # divs = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
                        # tmp_index = 100
                        # for div in divs:
                        #     tmp_title = div.find_element_by_xpath(".//a[1]").text
                        #     if str(word["short_title"]) in tmp_title:
                        #         tmp_index = divs.index(div)
                        #         break
                        # if tmp_index < 100:
                        #     su = driver.find_element_by_id("su")
                        #     ActionChains(driver).click(su).perform()
                        #     wait = WebDriverWait(driver, 3, 1)
                        #     wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
                        #     dest = divs[tmp_index]
                        #     driver.execute_script("arguments[0].scrollIntoView();", dest)
                        #     # 再向上移动200
                        #     js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                        #     driver.execute_script(js)
                        #     time.sleep(random.randint(2, 3))
                        #     a = dest.find_element_by_xpath(".//a[1]")
                        #     ActionChains(driver).click(a).perform()
                        #     windows = driver.window_handles
                        #     driver.switch_to.window(windows[-1])
                        #     self.last_step(word, driver)
                        # else:
                        #     driver.get(
                        #         "https://www.baidu.com/s?ie=UTF-8&wd=" + word[
                        #             "keyword"] + "&rn=3&si=" + self.site + "&ct=2097152")
                        #     # time.sleep(random.randint(2, 3))
                        #     # su = driver.find_element_by_id("su")
                        #     # ActionChains(driver).click(su).perform()
                        #     # wait = WebDriverWait(driver, 3, 1)
                        #     # # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
                        #     # wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
                        #     time.sleep(random.randint(2, 3))
                        #     divs = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
                        #     tmp_index = 100
                        #     for div in divs:
                        #         tmp_title = div.find_element_by_xpath(".//a[1]").text
                        #         if str(word["short_title"]) in tmp_title:
                        #             tmp_index = divs.index(div)
                        #             break
                        #     if tmp_index < 100:
                        #         su = driver.find_element_by_id("su")
                        #         ActionChains(driver).click(su).perform()
                        #         wait = WebDriverWait(driver, 3, 1)
                        #         wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
                        #         dest = divs[tmp_index]
                        #         driver.execute_script("arguments[0].scrollIntoView();", dest)
                        #         # 再向上移动200
                        #         js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                        #         driver.execute_script(js)
                        #         time.sleep(random.randint(2, 3))
                        #         a = dest.find_element_by_xpath(".//a[1]")
                        #         ActionChains(driver).click(a).perform()
                        #         windows = driver.window_handles
                        #         driver.switch_to.window(windows[-1])
                        #         self.last_step(word, driver)
                        #     else:
                        #         driver.quit()
                        #         # dest = divs[0]
                        #         # a = dest.find_element_by_xpath(".//a[1]")
                        #         # ActionChains(driver).click(a).perform()
                        #         # windows = driver.window_handles
                        #         # driver.switch_to.window(windows[-1])
                        #         # self.last_step(word, driver)
                else:
                    # 判断目标网站的地址需要为正好www.kf400.cn / 斜杠后面没有后缀的，判断这是第几名，就滚到【第几名 / 总位数】的位置，停留随机1~3秒.如果都是带后缀的内页就点击第一个带www.kf400.cn的目标网站
                    # 获取所有带目标网站的地址
                    dict1 = {}
                    dict2 = {}
                    all_divs = driver.find_elements_by_xpath("//div/h3")
                    ad_count = all_divs.__len__() - 10
                    divs = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
                    for div in divs:
                        divas = div.find_elements_by_xpath(".//div//a")
                        for diva in divas:
                            if diva.text == self.site + "/":
                                tmp = divs.index(div)
                                dict1[tmp] = diva.text
                            if self.site in diva.text:
                                tmp = divs.index(div)
                                dict2[tmp] = diva.text
                    if dict1.__len__() > 0:
                        index = sorted(dict1.items())[0][0]
                        dest = divs[index]
                        driver.execute_script("arguments[0].scrollIntoView();", dest)
                        # 再向上移动200
                        js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                        driver.execute_script(js)
                        time.sleep(random.randint(3, 5))

                        miaoshu = dest.find_element_by_xpath(".//div[@class='c-abstract']")
                        ActionChains(driver).click(miaoshu).perform()
                        time.sleep(random.randint(3, 5))

                        random_num = random.randint(1, 100)

                        if random.randint(1, 5) ==5:
                            # 标题
                            if random_num > 20:
                                index = sorted(dict1.items())[0][0]
                                dest = divs[index]
                                a = dest.find_element_by_xpath(".//a[1]")
                                ActionChains(driver).click(a).perform()
                                windows = driver.window_handles
                                driver.switch_to.window(windows[-1])
                                self.last_step(word, driver)
                            # 网址
                            elif random_num < 6:
                                index = sorted(dict1.items())[0][0]
                                dest = divs[index]
                                node_div = dest.find_elements_by_xpath("./div")
                                # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                if node_div.__len__() == 1:
                                    a = dest.find_element_by_xpath("./div[1]/div[2]/div[2]/a[1]")
                                    ActionChains(driver).click(a).perform()
                                    windows = driver.window_handles
                                    driver.switch_to.window(windows[-1])
                                    self.last_step(word, driver)
                                else:
                                    a = dest.find_element_by_xpath("./div[2]/a[1]")
                                    # ActionChains(driver).move_to_element(a).perform()
                                    # time.sleep(300)
                                    ActionChains(driver).click(a).perform()
                                    windows = driver.window_handles
                                    driver.switch_to.window(windows[-1])
                                    self.last_step(word, driver)
                        # 图片
                        else:

                            if random.randint(1, 5) == 5:
                                index = sorted(dict1.items())[0][0]
                                dest = divs[index]
                                # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                node_div = dest.find_elements_by_xpath("./div")
                                # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                if node_div.__len__() == 1:
                                    a = dest.find_element_by_xpath("./div[1]/div[1]/a[1]")
                                    ActionChains(driver).click(a).perform()
                                    windows = driver.window_handles
                                    driver.switch_to.window(windows[-1])
                                    self.last_step(word, driver)
                    else:
                        divs = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
                        dest = divs[0]
                        # miaoshu = dest.find_element_by_xpath(".//div[@class='c-abstract']")
                        # ActionChains(driver).click(miaoshu).perform()
                        # time.sleep(random.randint(3, 5))
                        driver.execute_script("arguments[0].scrollIntoView();", dest)
                        # 再向上移动200
                        js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                        driver.execute_script(js)
                        time.sleep(random.randint(2, 3))
                        random_num = random.randint(1, 100)
                        if random.randint(1, 5) ==5:
                            # 标题
                            if random_num > 20:
                                a = dest.find_element_by_xpath(".//a[1]")
                                ActionChains(driver).click(a).perform()
                                windows = driver.window_handles
                                driver.switch_to.window(windows[-1])
                                self.last_step(word, driver)
                            # 网址
                            elif random_num < 6:
                                node_div = dest.find_elements_by_xpath("./div")
                                # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                if node_div.__len__() == 1:
                                    a = dest.find_element_by_xpath("./div[1]/div[2]/div[2]/a[1]")
                                    ActionChains(driver).click(a).perform()
                                    windows = driver.window_handles
                                    driver.switch_to.window(windows[-1])
                                    self.last_step(word, driver)
                                else:
                                    a = dest.find_element_by_xpath("./div[2]/a[1]")
                                    # ActionChains(driver).move_to_element(a).perform()
                                    # time.sleep(300)
                                    ActionChains(driver).click(a).perform()
                                    windows = driver.window_handles
                                    driver.switch_to.window(windows[-1])
                                    self.last_step(word, driver)
                            # 图片
                            else:
                                # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                node_div = dest.find_elements_by_xpath("./div")
                                # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                                if node_div.__len__() == 1:
                                    a = dest.find_element_by_xpath("./div[1]/div[1]/a[1]")
                                    ActionChains(driver).click(a).perform()
                                    windows = driver.window_handles
                                    driver.switch_to.window(windows[-1])
                                    self.last_step(word, driver)

                # js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(random.randint(2, 5))
                # driver.execute_script(js)
                # time.sleep(random.randint(3, 5))
                #
                # # 判断目标网站的地址需要为正好www.kf400.cn / 斜杠后面没有后缀的，判断这是第几名，就滚到【第几名 / 总位数】的位置，停留随机1~3秒.如果都是带后缀的内页就点击第一个带www.kf400.cn的目标网站
                # # 获取所有带目标网站的地址
                # dict1 = {}
                # dict2 = {}
                # all_divs = driver.find_elements_by_xpath("//div/h3")
                # ad_count = all_divs.__len__() - 10
                # divs = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
                # for div in divs:
                #     divas = div.find_elements_by_xpath(".//div//a")
                #     for diva in divas:
                #         if diva.text == self.site + "/":
                #             tmp = divs.index(div)
                #             dict1[tmp] = diva.text
                #         if self.site in diva.text:
                #             tmp = divs.index(div)
                #             dict2[tmp] = diva.text
                # if dict1.__len__() > 0:
                #     index = sorted(dict1.items())[0][0]
                #     dest = divs[index]
                #     driver.execute_script("arguments[0].scrollIntoView();", dest)
                #     # 再向上移动200
                #     js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                #     driver.execute_script(js)
                #     time.sleep(random.randint(3, 5))
                #
                #     miaoshu = dest.find_element_by_xpath(".//div[@class='c-abstract']")
                #     ActionChains(driver).click(miaoshu).perform()
                #     time.sleep(random.randint(3, 5))
                #
                #     random_num = random.randint(1, 100)
                #     # 标题
                #     if random_num > 20:
                #         index = sorted(dict1.items())[0][0]
                #         dest = divs[index]
                #         a = dest.find_element_by_xpath(".//a[1]")
                #         ActionChains(driver).click(a).perform()
                #         windows = driver.window_handles
                #         driver.switch_to.window(windows[-1])
                #         self.last_step(word, driver)
                #     # 网址
                #     elif random_num < 6:
                #         index = sorted(dict1.items())[0][0]
                #         dest = divs[index]
                #         node_div = dest.find_elements_by_xpath("./div")
                #         # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                #         if node_div.__len__() == 1:
                #             a = dest.find_element_by_xpath("./div[1]/div[2]/div[2]/a[1]")
                #             ActionChains(driver).click(a).perform()
                #             windows = driver.window_handles
                #             driver.switch_to.window(windows[-1])
                #             self.last_step(word, driver)
                #         else:
                #             a = dest.find_element_by_xpath("./div[2]/a[1]")
                #             # ActionChains(driver).move_to_element(a).perform()
                #             # time.sleep(300)
                #             ActionChains(driver).click(a).perform()
                #             windows = driver.window_handles
                #             driver.switch_to.window(windows[-1])
                #             self.last_step(word, driver)
                #     # 图片
                #     else:
                #         index = sorted(dict1.items())[0][0]
                #         dest = divs[index]
                #         # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                #         node_div = dest.find_elements_by_xpath("./div")
                #         # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                #         if node_div.__len__() == 1:
                #             a = dest.find_element_by_xpath("./div[1]/div[1]/a[1]")
                #             ActionChains(driver).click(a).perform()
                #             windows = driver.window_handles
                #             driver.switch_to.window(windows[-1])
                #             self.last_step(word, driver)
                # elif dict2.__len__() > 0:
                #     index = sorted(dict2.items())[0][0]
                #     dest = divs[index]
                #     driver.execute_script("arguments[0].scrollIntoView();", dest)
                #     # 再向上移动200
                #     js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                #     driver.execute_script(js)
                #
                #     time.sleep(random.randint(3, 5))
                #     miaoshu = dest.find_element_by_xpath(".//div[@class='c-abstract']")
                #     ActionChains(driver).click(miaoshu).perform()
                #     time.sleep(random.randint(3, 5))
                #     random_num = random.randint(1, 100)
                #     # 标题
                #     if random_num > 20:
                #         index = sorted(dict2.items())[0][0]
                #         dest = divs[index]
                #         a = dest.find_element_by_xpath(".//a[1]")
                #         ActionChains(driver).click(a).perform()
                #         windows = driver.window_handles
                #         driver.switch_to.window(windows[-1])
                #         self.last_step(word, driver)
                #     # 网址
                #     elif random_num < 6:
                #         index = sorted(dict2.items())[0][0]
                #         dest = divs[index]
                #         node_div = dest.find_elements_by_xpath("./div")
                #         # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                #         if node_div.__len__() == 1:
                #             a = dest.find_element_by_xpath("./div[1]/div[2]/div[2]/a[1]")
                #             ActionChains(driver).click(a).perform()
                #             windows = driver.window_handles
                #             driver.switch_to.window(windows[-1])
                #             self.last_step(word, driver)
                #         else:
                #             a = dest.find_element_by_xpath("./div[2]/a[1]")
                #             ActionChains(driver).click(a).perform()
                #             windows = driver.window_handles
                #             driver.switch_to.window(windows[-1])
                #             self.last_step(word, driver)
                #     # 图片
                #     else:
                #         index = sorted(dict2.items())[0][0]
                #         dest = divs[index]
                #         # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                #         node_div = dest.find_elements_by_xpath("./div")
                #         # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                #         if node_div.__len__() == 1:
                #             a = dest.find_element_by_xpath("./div[1]/div[1]/a[1]")
                #             ActionChains(driver).click(a).perform()
                #             windows = driver.window_handles
                #             driver.switch_to.window(windows[-1])
                #             self.last_step(word, driver)
            except Exception as error:
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " error main process: " + str(error))
                if 'Connection aborted' in str(error):
                    delete_cookies.append(tmp_city_cookie)
                driver.quit()
                # print('traceback.print_exc():' + str(traceback.print_exc()))
        except Exception as error:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 2: " + str(error))
            # print('traceback.print_exc():' + str(traceback.print_exc()))

    def last_step(self, word, driver):
        global gids
        try:
            # driver.close()
            gids.append(word)
            # windows = driver.window_handles
            # driver.switch_to.window(windows[0])
            # driver.get('chrome://settings/clearBrowserData')
            # time.sleep(2)
            # clearData = driver.execute_script(
            #     "return document.querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page ').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog').querySelector('#clearBrowsingDataConfirm')")
            # time.sleep(1)
            # clearData.click()
            if self.ip_min == 1:
                time.sleep(30)
                driver.quit()
                return
            else:
                time.sleep(random.randint(60 * (self.ip_min - 1) - 10,
                                          60 * (self.ip_min - 1)) - self.sleep_time * self.arg_x)
            driver.close()
            windows = driver.window_handles
            driver.switch_to.window(windows[0])
            time.sleep(1)
            # su = driver.find_element_by_id("su")
            # ActionChains(driver).click(su).perform()
            js = "document.documentElement.scrollTop=document.documentElement.scrollTop+200"
            driver.execute_script(js)
            time.sleep(2)
            driver.quit()
        except Exception as error:
            if 'HTTPConnectionPool' not in str(error):
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " error last_step: " + str(error))
            driver.quit()


class Aclass(object):
    def __init__(self):
        self.fabaos = []
        self.citycookies = []
        self.cities = []
        self.ourcookies = {}

    def fetch_fabao(self, dba, batch_count):
        dba_ip = dba[0]
        dba_port = dba[1]
        dba_user = dba[2]
        dba_pwd = dba[3]
        engine = create_engine(
            'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session

        # sql = "select * from (select * from (select a.*,b.keyword as word from(select * from mipcms_fabao_list where state = 0  order by rand() limit " + batch_count+") a JOIN(select * from mipcms_fabao_list GROUP BY site,keyword)b on a.site = b.site ) c ORDER BY RAND()) d GROUP BY id"
        # cursor = session.execute(sql)
        cursor = session.execute(
            "select * from mipcms_fabao_list where state = 0  order by rand() limit " + batch_count)
        # cursor = session.execute(
        #     "select c.* from ( select a.*,b.mubiao from (select * from mipcms_fabao_history where time >= UNIX_TIMESTAMP(date_format(now(),'%Y-%m-%d'))) a  left join mipcms_fabao b on a.site = b.site and a.keyword=b.keyword where a.count<b.mubiao) c order by (mubiao * rand() ) desc limit 1000")

        result = cursor.fetchall()
        print(len(result))
        self.fabaos = result

        # save_objs = [
        #     {'id': obj.id, 'site': obj.site, 'keyword': obj.keyword, 'state': 2, 'short_title': obj.short_title} for
        #     obj in result]
        # session.bulk_update_mappings(Mipcms_fabao_list, save_objs)
        # session.commit()
        # session.close()

    def fetch_cities(self, dba):
        dba_ip = dba[0]
        dba_port = dba[1]
        dba_user = dba[2]
        dba_pwd = dba[3]
        engine = create_engine(
            'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        cursor = session.execute(
            "select name from mip_tags order by id")

        result = cursor.fetchall()
        print("city count :" + str(len(result)))
        self.cities = result

    def fetch_cookies(self, dba):
        dba_ip = dba[0]
        dba_port = dba[1]
        dba_user = dba[2]
        dba_pwd = dba[3]
        engine = create_engine(
            'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        all_count = session.query(func.count(City_cookies.id)).scalar()
        if all_count > 50000:
            x = random.randint(0, all_count - 50000)
        else:
            x = 0
        citycookies = session.query(City_cookies).limit(50000).offset(x).all()
        print("citycookies count :" + str(len(citycookies)))
        self.citycookies = citycookies

    def fetch_our_cookies(self, dba):
        dba_ip = dba[0]
        dba_port = dba[1]
        dba_user = dba[2]
        dba_pwd = dba[3]
        engine = create_engine(
            'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        sql = "select a.id,a.ua,a.city,a.zone,b.id as bid,b.domain,b.expiry,b.httpOnly,b.name,b.path,b.secure,b.value from (select * from cookie_list ORDER BY RAND() limit 100) a left join cookie_detail b on a.id = b.cookie_id"
        cursor = session.execute(sql)
        result = cursor.fetchall()
        print("our_cookies count :" + str(len(result)))
        dict = {}
        #先提取出id列表
        ids = []
        for i in result:
            if not i["id"] in ids:
                ids.append(i["id"])
        #找出id的对应字典
        for i in ids:
            list = []
            for j in result:
                if j["id"]==i:
                    list.append(j)
            dict[i]=list
        for ourcookie in dict:
            m = dict.get(ourcookie)
        self.ourcookies = dict
        ua = self.ourcookies[random.randint(0, aclass.ourcookies.__len__() - 1)].ua

    def fetch_mipcms_fabao_server_switch(self, dba):
        dba_ip = dba[0]
        dba_port = dba[1]
        dba_user = dba[2]
        dba_pwd = dba[3]
        engine = create_engine(
            'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        mipcms_fabao_server_switchs = session.query(Mipcms_fabao_server_switch).all()
        return mipcms_fabao_server_switchs[0].flag


def change_fbl(x, y):
    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsHeight = int(y)
    dm.PelsWidth = int(x)
    dm.BitsPerPel = 32
    dm.DisplayFixedOutput = 0
    win32api.ChangeDisplaySettings(dm, 0)


def close_chrome():
    try:
        process_list = list(psutil.process_iter())
        pids = []
        cmd_pids = []
        conhost_pids = []
        for p in process_list:
            if p.name() == "chrome.exe" and p.create_time() + 6 * 60 < time.time():
                pids.append(p.pid)
            if p.name() == "cmd.exe":
                cmd_pids.append(p)
            if p.name() == "conhost.exe":
                conhost_pids.append(p)
        print("close pids count:" + str(len(pids)))
        for pid in pids:
            try:
                os.system('taskkill /pid ' + str(pid) + ' /f')
            except Exception as error:
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 5: " + str(error))
        cmd_pids.sort(key=lambda x: x.create_time())
        conhost_pids.sort(key=lambda x: x.create_time())
        cmd_pids2 = cmd_pids[6:]
        conhost_pids3 = conhost_pids[8:]
        for pid in cmd_pids2:
            try:
                os.system('taskkill /pid ' + str(pid.pid) + ' /f')
            except Exception as error:
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 6: " + str(error))
        for pid in conhost_pids3:
            try:
                os.system('taskkill /pid ' + str(pid.pid) + ' /f')
            except Exception as error:
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 7: " + str(error))
    except Exception as error:
        print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 9: " + str(error))


def getMemCpu():
    data = psutil.virtual_memory()
    total = data.total  # 总内存,单位为byte
    free = data.available  # 可以内存
    # memory = "Memory usage:%d" % (int(round(data.percent))) + "%" + "  "
    memory = int(round(data.percent))
    # cpu = "CPU:%0.2f" % psutil.cpu_percent(interval=1) + "%"
    cpu = int(round(psutil.cpu_percent(interval=1)))
    return str(memory) + "," + str(cpu)


def getLocalSpace(folder):
    """
    获取磁盘剩余空间
    :param folder: 磁盘路径 例如 D:\\
    :return: 剩余空间 单位 G
    """
    folderTemp = folder
    if not os.path.exists(folderTemp):
        folderTemp = os.getcwd()
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folderTemp), None, None, ctypes.pointer(free_bytes))
        return str(100 - int(round(free_bytes.value * 100 / 1024 / 1024 / 1024 / 8)))
    else:
        st = os.statvfs(folderTemp)
        return str(100 - int(round(st.f_bavail * st.f_frsize * 100 / 1024 / 1024 / 8)))


if __name__ == '__main__':
    print("begin process")
    try:
        all_ips = []
        aliip = Aliip()
        this_time = 0
        tmp_uodate_count = 0
        readConfig = ReadConfig()
        num = readConfig.get_url()
        dba = readConfig.get_dba()
        dba_ip = dba[0]
        dba_port = dba[1]
        dba_user = dba[2]
        dba_pwd = dba[3]

        prams = readConfig.get_pram()
        get_window_size = readConfig.get_window_size()
        ip_min = prams[0]
        show_window = prams[1]
        open_chrome_sec = prams[2]
        pool_num = prams[3]
        server_id = prams[4]
        ip_address = prams[5]
        use_cookie = prams[6]
        batch_count = prams[7]
        commit_count = prams[8]
        sizelist = get_window_size.split(",")
        aclass = Aclass()
        engine = create_engine(
            'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        cursor = session.execute("update mipcms_fabao_server_switch set flag = 0")
        session.commit()
        try:
            aclass.fetch_our_cookies(dba)
            aclass.fetch_cookies(dba)
            aclass.fetch_cities(dba)
        except Exception as err:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + str(err))
            time.sleep(60)
        loop_count = 0
        while True:
            # close_chrome()
            try:
                flag = aclass.fetch_mipcms_fabao_server_switch(dba)
                if flag == 1:
                    break

            except Exception as err:
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + str(err))
                time.sleep(60)
            if len(not_exist_zone) > 0:
                filename = 'not_exist_zone.txt'
                with open(filename, 'a', encoding='utf8') as file_object:
                    for x in not_exist_zone:
                        file_object.write(x + "\n")
                    file_object.close()
            if len(gids) >= int(commit_count):
                aaa = gids
                try:
                    engine = create_engine(
                        'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
                    # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()  # 创建session
                    save_objs = [{'id': obj.id, 'site': obj.site, 'keyword': obj.keyword, 'state': 1,
                                  'short_title': obj.short_title} for
                                 obj in aaa]
                    session.bulk_update_mappings(Mipcms_fabao_list, save_objs)
                    session.commit()

                    # if len(update_cookies) > 0:
                    #     eee = []
                    #     for tmp in update_cookies:
                    #         if tmp != '':
                    #             eee.append(tmp.id)
                    #     fff = tuple(eee)
                    #     tmp_city_cookies = session.query(City_cookies).filter(City_cookies.id.in_(fff)).all()
                    #     save_objs = [
                    #         {'id': obj.id, 'cookie': obj.cookie, 'city': obj.city, 'error_count': obj.error_count + 1,
                    #          'zone': obj.zone, 'ua': obj.ua} for obj in
                    #         tmp_city_cookies]
                    #     session.bulk_update_mappings(City_cookies, save_objs)
                    #     session.commit()
                    #     update_cookies = []
                    # 顺便删除cookies
                    if len(delete_cookies) > 0:
                        bbb = []
                        for tmp in delete_cookies:
                            if tmp != '':
                                bbb.append(tmp.id)
                        ccc = tuple(bbb)
                        delete_count = session.query(City_cookies).filter(City_cookies.id.in_(ccc)).delete(
                            synchronize_session=False)
                        session.commit()
                        delete_cookies = []
                    session.close()
                except Exception as err:
                    time.sleep(60 * 10)
                    print(time.strftime("%Y-%m-%d %H:%M:%S") + " update db error " + str(err))
                for i in aaa:
                    print(i)
                success_count = success_count + len(gids)
                tmp_uodate_count = len(gids)
                submit_jiange_time = round(time.time() - submit_time)
                submit_time = time.time()
                dpan = getLocalSpace("D:\\")
                # 新增mipcms_fabao_server_record记录
                new_obj = Mipcms_fabao_server_record(ip_count=str(httpIP), success_count=str(success_count),
                                                     rate=str(round(100 * success_count / httpIP, 2)),
                                                     server_id=str(server_id), cpu=str(memCpu) + "," + str(dpan),
                                                     rate2=str(round(3600 * tmp_uodate_count / submit_jiange_time)),
                                                     dest_speed=str(3600 / int(open_chrome_sec)),
                                                     time=time.time(), ip_address=str(ip_address))
                session.add(new_obj)
                session.commit()
                # 新增mipcms_ip记录
                objects = []
                for ip in all_ips:
                    objects.append(Mipcms_ip(ip=ip['origin_ip'], city=ip['City'], county=ip['County']))
                session.bulk_save_objects(objects)
                session.commit()
                all_ips = []
                gids = []
            if len(aclass.fabaos) > 0 and len(aclass.fabaos[0]) > 0:
                # for mm in aclass.fabaos:
                #     gids.append(mm)
                # engine = create_engine(
                #     'mysql+mysqlconnector://' + dba_user + ':' + dba_pwd + '@' + dba_ip + ':' + dba_port + '/youpudb')
                # # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
                # DBSession = sessionmaker(bind=engine)
                # session = DBSession()  # 创建session
                # save_objs = [{'id': obj.id, 'site': obj.site, 'keyword': obj.keyword, 'state': 1,
                #               'short_title': obj.short_title} for
                #              obj in gids]
                # session.bulk_update_mappings(Mipcms_fabao_list, save_objs)
                # session.commit()

                try:
                    # aclass.fabaos.pop(0)
                    obj_fetchip = Fetchip(num, ip_min)
                    ips = obj_fetchip.requesturl()
                    loop_count = loop_count + 1
                    tmp_ips = []
                    for ip in ips:
                        if use_cookie == 'yes':
                            # 根据ip获取阿里ip的地域
                            ali_result = aliip.requesturl(ip["origin_ip"])
                            json_result = json.loads(ali_result)
                            ip["City"] = json_result["City"]
                            ip["County"] = json_result["County"]
                            all_ips.append(ip)

                            if json_result["City"] != '' and json_result["County"] != '':
                                tmp_ips.append(ip)
                        else:
                            ip["City"] = ip["city"]
                            ip["County"] = ''
                            all_ips.append(ip)
                            tmp_ips.append(ip)
                    # 这批ip使用10次
                    for n in range(int(pool_num)):
                        # for n in range(1):

                        threads = []
                        for ip in tmp_ips:
                            if len(aclass.fabaos) > 0:
                                # fabaos_one = aclass.fabaos.pop(0)
                                # fabaos_two = ""
                                # site = fabaos_one["site"]
                                # for word in aclass.fabaos:
                                #     if word["site"] == site:
                                #         fabaos_two = aclass.fabaos.pop(aclass.fabaos.index(word))
                                #         break
                                # one = oneThread(fabaos_one, fabaos_two, site,
                                #                 "--proxy-server=http://" + ip["ip"] + ":" + ip["port"], ip["origin_ip"],
                                #                 aclass.citycookies, show_window,
                                #                 "http://" + ip["ip"] + ":" + ip["port"], n,
                                #                 int(open_chrome_sec) * int(num), int(ip_min))

                                # 找出一个有此城市的关键词，再看province是否有
                                province = ip["province"]
                                city = ip["city"]
                                fabaos_tmp = ""
                                for fabao in aclass.fabaos:
                                    if city in fabao["keyword"]:
                                        fabaos_tmp = aclass.fabaos.pop(aclass.fabaos.index(fabao))
                                        break
                                if fabaos_tmp == "":
                                    for fabao in aclass.fabaos:
                                        if province in fabao["keyword"]:
                                            fabaos_tmp = aclass.fabaos.pop(aclass.fabaos.index(fabao))
                                            break
                                if fabaos_tmp == "":
                                    fabaos_tmp = aclass.fabaos.pop(0)
                                site = fabaos_tmp["site"]
                                #找所有的此site的对象
                                fabao_array = []
                                for fabao in aclass.fabaos:
                                    if site == fabao["site"]:
                                        fabao_array.append(fabao)
                                first_word =''
                                if len(fabao_array)>0:
                                    first_word = fabao_array[random.randint(0, len(fabao_array) - 1)]["keyword"]

                                if first_word =='':
                                    first_word = fabaos_tmp["keyword"]
                                #找出我们的cookie里是否有合适的，没有就不带cookie，有就80%概率用此城市的cookie，20%不带cookie
                                have_city = False
                                tmp_cookie = []
                                for ourcookie in aclass.ourcookies:
                                    if aclass.ourcookies.get(ourcookie)[0]["city"] == ip["City"] and aclass.ourcookies.get(ourcookie)[0]["zone"] == ip["County"]:
                                        tmp_cookie = aclass.ourcookies.pop(ourcookie)
                                        have_city = True

                                ua = ""
                                if have_city or random.randint(1,10)>2:
                                    use_cookie = "no"
                                    #找一个随机的ua
                                    ua = aclass.ourcookies[random.sample(aclass.ourcookies.keys(), 1)[0]][0]["ua"]

                                one = oneThread(fabaos_tmp, site,
                                                "--proxy-server=http://" + ip["ip"] + ":" + ip["port"], ip["origin_ip"],
                                                ip["City"], ip["County"],
                                                tmp_cookie, show_window,
                                                "http://" + ip["ip"] + ":" + ip["port"], n,
                                                int(open_chrome_sec) * int(num), int(ip_min), int(pool_num), use_cookie,
                                                aclass.cities,first_word,ua)
                                threads.append(one)
                        for thread in threads:
                            thread.start()
                            time.sleep(int(open_chrome_sec))
                    loop_jiange_time = abs(round(time.time() - loop_now_time) - int(this_time))
                    loop_now_time = time.time()
                    print("threads")
                    print(time.strftime("%Y-%m-%d %H:%M:%S") + " loop :  " + str(
                        loop_count) + " ; update_cookies :  " + str(len(update_cookies)))
                    if httpIP == 0 or submit_jiange_time == 0:
                        print(time.strftime("%Y-%m-%d %H:%M:%S") +
                              " httpIP --- : " + str(httpIP) + " ; success --- : " + str(
                            success_count) + " ; rate --- : 0 ;")
                        print(time.strftime("%Y-%m-%d %H:%M:%S") + " rate2 --- :0 ;" + " time --- " + str(this_time))
                    else:
                        print(time.strftime("%Y-%m-%d %H:%M:%S") +
                              " httpIP --- : " + str(httpIP) + " ; success --- : " + str(
                            success_count) + " ; rate --- : " + str(
                            round(100 * success_count / httpIP, 2)) + "% ;")
                        print(time.strftime("%Y-%m-%d %H:%M:%S") + " rate2 --- " + str(
                            round(3600 * tmp_uodate_count / submit_jiange_time)) + "; time --- " + str(this_time))
                except Exception as err:
                    print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 8: " + str(err))
                    # print('traceback.print_exc():' + str(traceback.print_exc()))
                time.sleep(120)
            else:
                print("fetchdb")
                try:
                    aclass.fetch_fabao(dba, batch_count)
                    if len(aclass.fabaos) > 0 and len(aclass.fabaos[0]) == 0:
                        gids = []
                        time.sleep(60 * 10)
                except Exception as err:
                    print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + str(err))
                    time.sleep(60)
                tmp = sizelist[random.randint(0, sizelist.__len__() - 1)]
                # change_fbl(tmp.split("*")[0], tmp.split("*")[1])
            # memCpu = getMemCpu()
            this_time = min(abs(loop_jiange_time - int(num) * int(open_chrome_sec) * int(pool_num)), 10)
            time.sleep(abs(int(this_time) - 2))
    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 4: " + str(err))
print("end process")
