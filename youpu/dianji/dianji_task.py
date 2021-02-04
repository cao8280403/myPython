#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column, String, create_engine, ForeignKey, func
from fetchip import Fetchip
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from db_class import Mipcms_fabao_history, Mipcms_fabao, City_cookies, Mipcms_fabao_list, Mipcms_fabao_server_record, \
    Mipcms_fabao_server_switch, Mipcms_ip
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


class oneThread(threading.Thread):
    # def __init__(self, word_one, word_two, site, arg1, ip, citycookies, show_window, proxies, n, arg_x, ip_min):
    def __init__(self, word_one, site, arg1, ip, city, county, citycookies, show_window, proxies, n, arg_x, ip_min):
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
        self.citycookies = citycookies
        self.show_window = show_window
        self.proxies = proxies
        self.sleep_time = n
        self.arg_x = arg_x
        self.ip_min = ip_min

    def run(self):
        global delete_cookies
        global update_cookies
        global httpIP
        global not_exist_zone
        word = self.word_one
        try:
            # 初始化的时候 需要获取ip and port 设置ua 使用传递过来的参数ua
            # print("begin thread：")
            options = webdriver.ChromeOptions()  # 设置代理
            options.add_argument(self.arg1)
            options.add_argument('lang=zh_CN.UTF-8')
            options.add_argument('--disk-cache-dir=d:\chromecahce')
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
            # # 如果地域不全，就随机拿个ua，否则根据城市和地区选一个随机的cookie
            # cookie_list_str = ''
            tmp_city_cookie = ''
            # ua = ""
            # cookie_flag = True
            tmp_cookies = []
            for tmp in self.citycookies:
                if tmp.city == self.city and tmp.zone == self.county:
                    tmp_cookies.append(tmp)
            if tmp_cookies.__len__() == 1:
                city_cookie = tmp_cookies[0]
                ua = city_cookie.ua
                tmp_city_cookie = city_cookie
                cookie_list_str = city_cookie.cookie
            elif tmp_cookies.__len__() == 0:
                return
                # ua = self.citycookies[random.randint(0, len(self.citycookies) - 1)].ua
                # cookie_flag = False
                # not_exist_zone.append(json_result["City"] + "--" + json_result["County"])
            else:
                city_cookie = tmp_cookies[random.randint(0, tmp_cookies.__len__() - 1)]
                ua = city_cookie.ua
                tmp_city_cookie = city_cookie
                cookie_list_str = city_cookie.cookie
            # if json_result["City"] != '' and json_result["County"] != '':
            #     tmp_cookies = []
            #     for tmp in self.citycookies:
            #         if tmp.city == json_result["City"] and tmp.zone == json_result["County"]:
            #             tmp_cookies.append(tmp)
            #     if tmp_cookies.__len__() == 1:
            #         city_cookie = tmp_cookies[0]
            #         ua = city_cookie.ua
            #         tmp_city_cookie = city_cookie
            #         cookie_list_str = city_cookie.cookie
            #     elif tmp_cookies.__len__() == 0:
            #         return
            #         # ua = self.citycookies[random.randint(0, len(self.citycookies) - 1)].ua
            #         # cookie_flag = False
            #         # not_exist_zone.append(json_result["City"] + "--" + json_result["County"])
            #     else:
            #         city_cookie = tmp_cookies[random.randint(0, tmp_cookies.__len__() - 1)]
            #         ua = city_cookie.ua
            #         tmp_city_cookie = city_cookie
            #         cookie_list_str = city_cookie.cookie
            # else:
            #     return
            #     # cookie_flag = False
            #     # ua = self.citycookies[random.randint(0, len(self.citycookies) - 1)].ua
            # 'user-agent="' + ua[random.randint(0, ua.__len__() - 1)][0] + '"',
            options.add_argument('user-agent="' + ua + '"')
            options.add_argument('Connection="close"')
            driver = webdriver.Chrome(options=options)
            try:
                httpIP = httpIP + 1
                driver.get("https://www.baidu.com")
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="su"]'))
                )
                if cookie_list_str != '':
                    driver.delete_all_cookies()
                    cookie_list_array = cookie_list_str.split(";")
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
                    delete_cookies.append(tmp_city_cookie)
                driver.get(
                    "https://www.baidu.com/s?ie=UTF-8&wd=" + word["keyword"] + "&si=" + self.site + "&ct=2097152")
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="su"]'))
                )

                time.sleep(random.randint(1, 3))
                su = driver.find_element_by_id("su")
                ActionChains(driver).click(su).perform()
                wait = WebDriverWait(driver, 3, 1)
                # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
                wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))

                try:
                    proxies = {'http': self.proxies}
                    # 恶意访问将ip拉入黑名单
                    for t in range(7):
                        time.sleep(0.1)
                        r = requests.get("http://" + self.site + "/shell.php", proxies=proxies, timeout=3)
                except Exception as error:
                    print("error attack: " + str(error))
                time.sleep(random.randint(3, 5))
                js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(random.randint(2, 5))
                driver.execute_script(js)
                time.sleep(random.randint(3, 5))

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
                elif dict2.__len__() > 0:
                    index = sorted(dict2.items())[0][0]
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
                    # 标题
                    if random_num > 20:
                        index = sorted(dict2.items())[0][0]
                        dest = divs[index]
                        a = dest.find_element_by_xpath(".//a[1]")
                        ActionChains(driver).click(a).perform()
                        windows = driver.window_handles
                        driver.switch_to.window(windows[-1])
                        self.last_step(word, driver)
                    # 网址
                    elif random_num < 6:
                        index = sorted(dict2.items())[0][0]
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
                            ActionChains(driver).click(a).perform()
                            windows = driver.window_handles
                            driver.switch_to.window(windows[-1])
                            self.last_step(word, driver)
                    # 图片
                    else:
                        index = sorted(dict2.items())[0][0]
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
            except Exception as error:
                if 'Connection aborted' in str(error):
                    delete_cookies.append(tmp_city_cookie)
                driver.quit()
                print(time.strftime("%Y-%m-%d %H:%M:%S") + " error main process: " + str(error))
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
            time.sleep(random.randint(60 * (self.ip_min - 1) - 10,
                                      60 * (self.ip_min - 1)) - self.sleep_time * self.arg_x)
            windows = driver.window_handles
            driver.switch_to.window(windows[0])
            time.sleep(1)
            su = driver.find_element_by_id("su")
            ActionChains(driver).click(su).perform()
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

    def fetch_fabao(self):
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session

        cursor = session.execute(
            "select * from mipcms_fabao_list where state = 0  order by rand() limit 1000")
        # cursor = session.execute(
        #     "select c.* from ( select a.*,b.mubiao from (select * from mipcms_fabao_history where time >= UNIX_TIMESTAMP(date_format(now(),'%Y-%m-%d'))) a  left join mipcms_fabao b on a.site = b.site and a.keyword=b.keyword where a.count<b.mubiao) c order by (mubiao * rand() ) desc limit 1000")

        result = cursor.fetchall()
        print(len(result))
        self.fabaos = result

        save_objs = [{'id': obj.id, 'site': obj.site, 'keyword': obj.keyword, 'state': 2} for
                     obj in result]
        session.bulk_update_mappings(Mipcms_fabao_list, save_objs)
        session.commit()
        session.close()

    def fetch_cookies(self):
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        all_count = session.query(func.count(City_cookies.id)).scalar()
        if all_count > 50000:
            x = random.randint(0, all_count - 50000)
        else:
            x = 0
        citycookies = session.query(City_cookies).limit(50000).offset(x).all()
        print(len(citycookies))
        self.citycookies = citycookies

    def fetch_mipcms_fabao_server_switch(self):
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
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
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        cursor = session.execute("update mipcms_fabao_server_switch set flag = 0")
        session.commit()
        try:
            aclass.fetch_cookies()
        except Exception as err:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + str(err))
            time.sleep(60)
        loop_count = 0
        while True:
            close_chrome()
            try:
                flag = aclass.fetch_mipcms_fabao_server_switch()
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
            if len(gids) >= 200:
                aaa = gids
                try:
                    engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
                    # engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@wtc.cn:3306/youpudb')
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()  # 创建session
                    save_objs = [{'id': obj.id, 'site': obj.site, 'keyword': obj.keyword, 'state': 1} for
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
                memCpu = getMemCpu()
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
                try:
                    # aclass.fabaos.pop(0)
                    obj_fetchip = Fetchip(num, ip_min)
                    ips = obj_fetchip.requesturl()
                    loop_count = loop_count + 1
                    tmp_ips = []
                    for ip in ips:
                        # 根据ip获取阿里ip的地域
                        ali_result = aliip.requesturl(ip["origin_ip"])
                        json_result = json.loads(ali_result)
                        ip["City"] = json_result["City"]
                        ip["County"] = json_result["County"]
                        all_ips.append(ip)

                        if json_result["City"] != '' and json_result["County"] != '':
                            tmp_ips.append(ip)
                    # 这批ip使用10次
                    for n in range(int(pool_num)):

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
                                one = oneThread(fabaos_tmp, site,
                                                "--proxy-server=http://" + ip["ip"] + ":" + ip["port"], ip["origin_ip"],
                                                ip["City"], ip["County"],
                                                aclass.citycookies, show_window,
                                                "http://" + ip["ip"] + ":" + ip["port"], n,
                                                int(open_chrome_sec) * int(num), int(ip_min))
                                threads.append(one)
                        for thread in threads:
                            time.sleep(int(open_chrome_sec))
                            thread.start()
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
                # time.sleep(120)
            else:
                print("fetchdb")
                try:
                    aclass.fetch_fabao()
                    if len(aclass.fabaos) > 0 and len(aclass.fabaos[0]) == 0:
                        gids = []
                        time.sleep(60 * 10)
                except Exception as err:
                    print(time.strftime("%Y-%m-%d %H:%M:%S") + " " + str(err))
                    time.sleep(60)
                tmp = sizelist[random.randint(0, sizelist.__len__() - 1)]
                change_fbl(tmp.split("*")[0], tmp.split("*")[1])
            this_time = min(abs(loop_jiange_time - int(num) * int(open_chrome_sec) * int(pool_num)), 10)
            time.sleep(abs(int(this_time) - 2))
    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S") + " error 4: " + str(err))
print("end process")
