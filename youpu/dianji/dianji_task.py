from sqlalchemy import Column, String, create_engine, ForeignKey, func
from fetchip import Fetchip
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from db_class import Mipcms_fabao_history, Mipcms_fabao, City_cookies
from aliip import Aliip
from dianji_thread import Dianji_thread
import time
import threading
from selenium import webdriver  # 浏览器驱动器
from selenium.webdriver.common.by import By  # 定位器
from selenium.webdriver.common.keys import Keys  # 键盘对象
from selenium.webdriver.support import expected_conditions as EC  # 判断器
from selenium.webdriver.support.wait import WebDriverWait  # 浏览器等待对像
from selenium.webdriver.chrome.service import Service
import time
import json
import os
import random
from selenium.webdriver.common.action_chains import ActionChains
import threading
from aliip import Aliip
from Bclass import Bclass
import psutil

gids = []
delete_cookies = []


class oneThread(threading.Thread):
    def __init__(self, word_one, word_two, site, arg1, ip, citycookies):
        threading.Thread.__init__(self)
        self.word_one = word_one
        if word_two != "":
            self.word_two = word_two
        else:
            self.word_two = ""
        self.site = site
        self.arg1 = arg1
        self.ip = ip
        self.citycookies = citycookies

    def run(self):
        global delete_cookies
        try:
            # 初始化的时候 需要获取ip and port 设置ua 使用传递过来的参数ua
            # print("begin thread：")
            options = webdriver.ChromeOptions()  # 设置代理
            options.add_argument(self.arg1)
            options.add_argument('lang=zh_CN.UTF-8')
            # options.add_argument('--ignore-certificate-errors')
            # options.add_argument('--disable-infobars')  # 不显示正在受自动化软件控制  失效
            options.headless = True
            options.add_argument('log-level=3')
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
            options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示正在受自动化软件控制#跟上面只能选一个
            # 根据ip获取阿里ip的地域
            aliip = Aliip()
            ali_result = aliip.requesturl(self.ip)
            json_result = json.loads(ali_result)
            # 如果地域不全，就随机拿个ua，否则根据城市和地区选一个随机的cookie
            cookie_list_str = ''
            tmp_city_cookie = ''
            ua = ""
            if json_result["City"] != '' and json_result["County"] != '':
                tmp_cookies = []
                for tmp in self.citycookies:
                    if tmp.city == json_result["City"] and tmp.zone == json_result["County"]:
                        tmp_cookies.append(tmp)
                city_cookie = tmp_cookies[random.randint(0, tmp_cookies.__len__() - 1)]
                ua = city_cookie.ua
                tmp_city_cookie = city_cookie
                cookie_list_str = city_cookie.cookie
            else:
                ua = self.citycookies[random.randint(0, len(self.citycookies) - 1)].ua
            # 'user-agent="' + ua[random.randint(0, ua.__len__() - 1)][0] + '"',
            options.add_argument('user-agent="' + ua + '"')
            options.add_argument('Connection="close"')
            driver = webdriver.Chrome(options=options)
            try:
                # driver.set_window_size(self.arg3, self.arg4)  # 分辨率 1024*768
                # driver.maximize_window()

                driver.get("https://www.baidu.com")
                driver.delete_all_cookies()

                if cookie_list_str != '':
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
                # print_time(self.name, self.counter, 5)
                random_count = self.one_circle(self.word_one, "1", driver)

                if random_count == 1:
                    time.sleep(random.randint(30, 100))
                    windows = driver.window_handles
                    if windows.__len__() == 2:
                        driver.switch_to.window(windows[-1])  # 切换到新窗口
                        # print(driver.window_handles)  # 查看所有window handles
                        driver.close()
                        driver.switch_to.window(windows[0])
                        # 关闭第二个页面，回到第一个页面，鼠标移动到搜索输入框，点击一下，按键盘删除10下，每下间隔0.1~0.3秒
                        inputs = driver.find_element_by_id("kw")
                        ActionChains(driver).click(inputs).perform()
                        for i in range(10):
                            inputs.send_keys(Keys.BACKSPACE)
                            time.sleep(random.randint(1, 3) / 10)
                        if self.word_two != "":
                            self.one_circle(self.word_two, "2", driver)
                    elif windows.__len__() == 1:
                        # driver.switch_to.window(windows[-1])  # 切换到新窗口
                        # print(driver.window_handles)  # 查看所有window handles
                        # driver.close()
                        # driver.switch_to.window(windows[0])
                        # 关闭第二个页面，回到第一个页面，鼠标移动到搜索输入框，点击一下，按键盘删除10下，每下间隔0.1~0.3秒
                        inputs = driver.find_element_by_id("kw")
                        ActionChains(driver).click(inputs).perform()
                        for i in range(10):
                            inputs.send_keys(Keys.BACKSPACE)
                            time.sleep(random.randint(1, 3) / 10)
                        if self.word_two != "":
                            self.one_circle(self.word_two, "2", driver)
                            # print("two circle over")
                        # else:
                        #     a = 1
                        #     print("only one circle over")
                # 修改关键词后再次执行方法one_circle
                # print("end thread：")

            except Exception as err:
                a = 1
                print("error 1: " + str(err))
                # print("ua ===>"+ua)
                # print("cookie ===>"+cookie_list_str)
                delete_cookies.append(tmp_city_cookie)
                # os.system("taskkill /f  chromedriver.exe")
                # os.system('taskkill /im chromedriver.exe /F')
                # os.system('taskkill /pid chromedriver.exe /f')
                # os.system('taskkill /im chromedriver.exe /F')
                # os.system('taskkill /im chrome.exe /F')
                print(driver.window_handles)  # 查看所有window handles
                # driver.close()
                driver.quit()

            driver.quit()
        except Exception as err:
            a = 1
            print("error 2: " + str(err))

    def one_circle(self, word, count, driver):
        try:
            # print("begin circle：word is " + word + " count is " + count)

            self.normal_step(word, count, driver)
            # 最后的走向判断
            if count == "2":
                return 2
            else:
                return 1
                # 随机返回一个值
                # random_count = random.randint(0, 1)
                # if random_count == 1:
                #     print("return 1")
                #     return 1
                # else:
                #     print("go on")
                #     return 0
        except Exception as err:
            a = 1
            # print(err)

    def normal_step(self, word, count, driver):
        global gids
        try:
            # print("normal_step")

            inputs = driver.find_element_by_id("kw")
            for keyword in word["keyword"]:
                inputs.send_keys(keyword)
                random_count = random.randint(1, 10)
                time.sleep(random_count / 10)
            time.sleep(random.randint(1, 2))
            # inputs.send_keys("联通电话费查询")
            su = driver.find_element_by_id("su")
            time.sleep(random.randint(0, 1))
            ActionChains(driver).click(su).perform()
            time.sleep(random.randint(1, 3))
            wait = WebDriverWait(driver, 10, 0.5)
            # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
            wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
            if count == "1":
                # print(1)
                newurl = driver.current_url + '&si=' + self.site + "&ct=2097152"
                driver.get(newurl)
                wait = WebDriverWait(driver, 10, 0.5)
                # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
                wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
            # else:
            #     print(2)
            # 判断第一页是否有广告，没有则点百度一下，再下一页，上一页，后面只点百度一下重复五次
            # guanggaos = driver.find_elements_by_xpath("//span[@data-tuiguang]")
            # if guanggaos.__len__() == 0:
            #     time.sleep(random.randint(2, 5))
            #     su = driver.find_element_by_id("su")
            #     ActionChains(driver).click(su).perform()
            #     guanggaos = driver.find_elements_by_xpath("//span[@data-tuiguang]")
            #     if guanggaos.__len__() == 0:
            #         time.sleep(random.randint(1, 3))
            #         js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(random.randint(2, 6))
            #         driver.execute_script(js)
            #         time.sleep(random.randint(1, 3))
            #         js = "document.documentElement.scrollTop=document.body.scrollHeight"
            #         driver.execute_script(js)
            #         # 点下一页
            #         time.sleep(random.randint(1, 3))
            #         next_page = driver.find_elements_by_xpath("//a[@class='n']")[0]
            #         ActionChains(driver).click(next_page).perform()
            #         # windows = driver.window_handles
            #         # driver.switch_to.window(windows[-1])  # 切换到新窗口
            #         js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(random.randint(2, 6))
            #         driver.execute_script(js)
            #         pre_page = driver.find_elements_by_xpath("//a[@class='n']")[0]
            #         ActionChains(driver).click(pre_page).perform()
            #         for p in range(20):
            #             time.sleep(random.randint(2, 4))
            #             su = driver.find_element_by_id("su")
            #             ActionChains(driver).click(su).perform()
            #             guanggaos = driver.find_elements_by_xpath("//span[@data-tuiguang]")
            #             if guanggaos.__len__() > 0:
            #                 break

            # 找到第一个元素，看是否有保障和向下按钮
            one = driver.find_element_by_xpath("//div[@id='content_left']/div[@data-click][1]")
            c_tools = one.find_elements_by_xpath(".//div[@class='c-tools']")  # 向下
            data_baobiao = one.find_elements_by_xpath(".//a[@data-baobiao]")  # 广告的保障
            data_bao = one.find_elements_by_xpath(".//span[@data-bao]")  # 普通的保障
            # 如果存在保障就有概率去点
            # 50 % 几率鼠标移动到第一个的【保障】，悬停1~2秒
            if len(data_baobiao) + len(data_bao) > 0:
                if random.randint(1, 2) == 1:
                    if len(data_baobiao) > 0:
                        baobiao = data_baobiao[0]
                        ActionChains(driver).move_to_element(baobiao).perform()
                        time.sleep(random.randint(1, 2))
                    if len(data_bao) > 0:
                        bao = data_bao[0]
                        ActionChains(driver).move_to_element(bao).perform()
                        time.sleep(random.randint(1, 2))

            # 20 % 几率鼠标移动到第一个【向下按钮】，悬停1~2秒
            if len(c_tools) > 0:
                if random.randint(1, 5) == 1:
                    xiangxia = c_tools[0]
                    ActionChains(driver).move_to_element(xiangxia).perform()
                    time.sleep(random.randint(1, 2))

            # 判断第一条是不是广告，不是就不用点了 data-ecimtimesign style
            one = driver.find_element_by_xpath("//div[@id='content_left']/div[@data-click][1]")
            if one.get_attribute("style") != '':
                # 50 % 几率点击第1条的标题位置，1~3秒后关闭
                if random.randint(1, 2) == 1:
                    a1 = one.find_element_by_xpath(".//a[1]")
                    ActionChains(driver).click(a1).perform()
                    time.sleep(random.randint(1, 3))
                    windows = driver.window_handles
                    driver.switch_to.window(windows[-1])
                    driver.close()
                    driver.switch_to.window(windows[0])
                    time.sleep(random.randint(1, 3))
                # 20 % 几率点击第2条的标题位置，1~3秒后关闭
                if random.randint(1, 5) == 1:
                    a1 = driver.find_element_by_xpath("//div[@id='content_left']/div[2]//a[1]")
                    ActionChains(driver).click(a1).perform()
                    time.sleep(random.randint(1, 3))
                    windows = driver.window_handles
                    driver.switch_to.window(windows[-1])
                    driver.close()
                    driver.switch_to.window(windows[0])
                    time.sleep(random.randint(1, 3))
            # 执行向下滚动1次，幅度随机20 % ~60 % 高度，后停留1~3秒
            now_height = random.randint(2, 6)
            js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
            driver.execute_script(js)
            time.sleep(random.randint(1, 3))
            # 执行1-5次的滚动（50%上滚、50%下滚），幅度为随机20%~60%的高度，每次滚动后停留随机1~3秒
            for i in range(random.randint(1, 5)):
                if random.randint(1, 2) == 1:
                    now_height = min(now_height + random.randint(1, 5), 10)
                    if now_height == 0:
                        js = "document.documentElement.scrollTop=document.body.scrollTop"
                    else:
                        js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                    print(js)
                    driver.execute_script(js)
                    time.sleep(random.randint(1, 3))
                else:
                    tmp = random.randint(1, 5)
                    now_height = now_height - tmp if now_height > tmp else 0
                    if now_height == 0:
                        js = "document.documentElement.scrollTop=document.body.scrollTop"
                    else:
                        js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                    print(js)
                    driver.execute_script(js)
                    time.sleep(random.randint(1, 3))
            js = "document.documentElement.scrollTop=document.body.scrollTop"
            driver.execute_script(js)
            # 判断目标网站的地址需要为正好www.kf400.cn / 斜杠后面没有后缀的，判断这是第几名，就滚到【第几名 / 总位数】的位置，停留随机1~3秒.如果都是带后缀的内页就点击第一个带www.kf400.cn的目标网站
            # 获取所有带目标网站的地址
            time.sleep(random.randint(2, 3))
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
                # js = "alert(document.body.scrollTop)"
                # driver.execute_script(js)
                # js = "alert(document.body.scrollHeight)"
                # driver.execute_script(js)
                # if (index + ad_count - 1) > 2:
                #     js = "document.documentElement.scrollTop=document.body.scrollHeight*" + str(
                #         (index + ad_count - 2) / all_divs.__len__())
                #     driver.execute_script(js)

                random_num = random.randint(1, 100)
                # 标题
                if random_num > 20:
                    index = sorted(dict1.items())[0][0]
                    dest = divs[index]
                    a = dest.find_element_by_xpath(".//a[1]")
                    ActionChains(driver).click(a).perform()
                    # threadLock.acquire()
                    # self.bclass = Bclass()
                    # self.bclass.add(word)
                    # threadLock.release()
                    gids.append(word)
                    time.sleep(random.randint(1, 3))
                # 网址
                elif random_num < 6:
                    index = sorted(dict1.items())[0][0]
                    dest = divs[index]
                    node_div = dest.find_elements_by_xpath("./div")
                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                    if node_div.__len__() == 1:
                        a = dest.find_element_by_xpath("./div[1]/div[2]/div[2]/a[1]")
                        # ActionChains(driver).move_to_element(a).perform()
                        # time.sleep(300)
                        ActionChains(driver).click(a).perform()
                        # threadLock.acquire()
                        # self.bclass = Bclass()
                        # self.bclass.add(word)
                        # threadLock.release()
                        gids.append(word)
                        time.sleep(random.randint(1, 3))
                    else:
                        a = dest.find_element_by_xpath("./div[2]/a[1]")
                        # ActionChains(driver).move_to_element(a).perform()
                        # time.sleep(300)
                        ActionChains(driver).click(a).perform()
                        # threadLock.acquire()
                        # self.bclass = Bclass()
                        # self.bclass.add(word)
                        # threadLock.release()
                        gids.append(word)
                        time.sleep(random.randint(1, 3))

                # 图片
                else:
                    index = sorted(dict1.items())[0][0]
                    dest = divs[index]
                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                    node_div = dest.find_elements_by_xpath("./div")
                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                    if node_div.__len__() == 1:
                        a = dest.find_element_by_xpath("./div[1]/div[1]/a[1]")
                        # ActionChains(driver).move_to_element(a).perform()
                        # time.sleep(300)
                        ActionChains(driver).click(a).perform()
                        time.sleep(random.randint(1, 3))
            elif dict2.__len__() > 0:
                index = sorted(dict2.items())[0][0]
                dest = divs[index]
                driver.execute_script("arguments[0].scrollIntoView();", dest)
                # 再向上移动200
                js = "document.documentElement.scrollTop=document.documentElement.scrollTop<=200?document.body.scrollTop:document.documentElement.scrollTop-200"
                driver.execute_script(js)
                time.sleep(random.randint(1, 3))
                random_num = random.randint(1, 100)
                # 标题
                if random_num > 20:
                    index = sorted(dict2.items())[0][0]
                    dest = divs[index]
                    a = dest.find_element_by_xpath(".//a[1]")
                    ActionChains(driver).click(a).perform()
                    # threadLock.acquire()
                    # self.bclass = Bclass()
                    # self.bclass.add(word)
                    # threadLock.release()
                    gids.append(word)
                    time.sleep(random.randint(1, 3))
                # 网址
                elif random_num < 6:
                    index = sorted(dict2.items())[0][0]
                    dest = divs[index]
                    node_div = dest.find_elements_by_xpath("./div")
                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                    if node_div.__len__() == 1:
                        a = dest.find_element_by_xpath("./div[1]/div[2]/div[2]/a[1]")
                        # ActionChains(driver).move_to_element(a).perform()
                        # time.sleep(300)
                        ActionChains(driver).click(a).perform()
                        # threadLock.acquire()
                        # self.bclass = Bclass()
                        # self.bclass.add(word)
                        # threadLock.release()
                        gids.append(word)
                        time.sleep(random.randint(1, 3))
                    else:
                        a = dest.find_element_by_xpath("./div[2]/a[1]")
                        # ActionChains(driver).move_to_element(a).perform()
                        # time.sleep(300)
                        ActionChains(driver).click(a).perform()
                        # threadLock.acquire()
                        # self.bclass = Bclass()
                        # self.bclass.add(word)
                        # threadLock.release()
                        gids.append(word)
                        time.sleep(random.randint(1, 3))

                # 图片
                else:
                    index = sorted(dict2.items())[0][0]
                    dest = divs[index]
                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                    node_div = dest.find_elements_by_xpath("./div")
                    # 判断子节点div的个数，个数为1就是有图片，个数为2就是没有图片
                    if node_div.__len__() == 1:
                        a = dest.find_element_by_xpath("./div[1]/div[1]/a[1]")
                        # ActionChains(driver).move_to_element(a).perform()
                        # time.sleep(300)
                        ActionChains(driver).click(a).perform()
                        # threadLock.acquire()
                        # self.bclass = Bclass()
                        # self.bclass.add(word)
                        # threadLock.release()
                        gids.append(word)
                        time.sleep(random.randint(1, 3))
        except Exception as err:
            a = 1
            driver.quit()
            print("error 3: " + str(err))


class Aclass(object):
    def __init__(self):
        self.fabaos = []
        self.citycookies = []

    def fetch_fabao(self):
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        cursor = session.execute(
            "select a.* from (select * from mipcms_fabao_history where time > UNIX_TIMESTAMP(date_format(now(),'%Y-%m-%d'))) a  left join mipcms_fabao b on a.site = b.site and a.keyword=b.keyword and a.count<b.mubiao order by rand()")
        result = cursor.fetchall()
        print(len(result))
        self.fabaos = result

    def fetch_cookies(self):
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        citycookies = session.query(City_cookies).all()
        print(len(citycookies))
        self.citycookies = citycookies


def close_chrome():
    process_list = list(psutil.process_iter())
    pids = []
    for p in process_list:
        if p.name() == "chrome.exe" and p.create_time() + 3 * 60 < time.time():
            pids.append(p.pid)
    print("close pids count:"+str(len(pids)))
    for pid in pids:
        os.system('taskkill /pid '+str(pid)+' /f')


if __name__ == '__main__':
    print("begin process")
    try:
        aclass = Aclass()
        aclass.fetch_cookies()
        while True:
            close_chrome()
            if len(gids) >= 10:
                aaa = gids
                try:
                    engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
                    DBSession = sessionmaker(bind=engine)
                    session = DBSession()  # 创建session
                    save_objs = [{'id': obj.id, 'site': obj.site, 'keyword': obj.keyword, 'count': obj.count + 1,
                                  'time': obj.time} for obj in
                                 gids]
                    session.bulk_update_mappings(Mipcms_fabao_history, save_objs)
                    session.commit()
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
                        print(delete_count)
                except Exception as err:
                    print(err)
                for i in aaa:
                    print(i)
                gids = []
            if len(aclass.fabaos) > 0 and len(aclass.fabaos[0]) > 0:
                # aclass.fabaos.pop(0)
                obj_fetchip = Fetchip()
                ips = obj_fetchip.requesturl()
                threads = []
                for ip in ips:
                    if len(aclass.fabaos) > 0:
                        fabaos_one = aclass.fabaos.pop(0)
                        fabaos_two = ""
                        site = fabaos_one["site"]
                        for word in aclass.fabaos:
                            if word["site"] == site:
                                fabaos_two = aclass.fabaos.pop(aclass.fabaos.index(word))
                                break
                        one = oneThread(fabaos_one, fabaos_two, site,
                                        "--proxy-server=http://" + ip["ip"] + ":" + ip["port"], ip["origin_ip"],
                                        aclass.citycookies)
                        threads.append(one)
                for thread in threads:
                    # time.sleep(1)
                    thread.start()
                print("threads")
                time.sleep(10)
            else:
                print("fetchdb")
                aclass.fetch_fabao()
    except Exception as err:
        print("error 4: " + str(err))
print("end process")
