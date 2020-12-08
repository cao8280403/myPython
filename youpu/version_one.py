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
        driver = webdriver.Chrome()
        driver.get("https://www.baidu.com")
        driver.delete_all_cookies()
        # print_time(self.name, self.counter, 5)
        random_count = self.one_circle(self.words[0], "1", driver)

        if random_count == 1:
            time.sleep(random.randint(3, 20))
            windows = driver.window_handles
            if windows.__len__() == 2:
                driver.switch_to.window(windows[-1])  # 切换到新窗口
                print(driver.window_handles)  # 查看所有window handles
                driver.close()
                driver.switch_to.window(windows[0])
                # 关闭第二个页面，回到第一个页面，鼠标移动到搜索输入框，点击一下，按键盘删除10下，每下间隔0.1~0.3秒
                inputs = driver.find_element_by_id("kw")
                ActionChains(driver).click(inputs).perform()
                for i in range(10):
                    inputs.send_keys(Keys.BACKSPACE)
                    time.sleep(random.randint(1, 3) / 10)
                self.one_circle(self.words[1], "2", driver)
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
                self.one_circle(self.words[1], "2", driver)
            print("two circle over")
        else:
            print("only one circle over")
        # 修改关键词后再次执行方法one_circle
        print("end thread：")
        driver.quit()

    def one_circle(self, word, count, driver):
        print("begin circle：word is " + word + " count is " + count)

        self.normal_step(word, driver)
        # 最后的走向判断
        if count == "2":
            return 2
        else:
            # 随机返回一个值
            random_count = random.randint(0, 1)
            if random_count == 1:
                print("return 1")
                return 1
            else:
                print("go on")
                return 0

    def normal_step(self, word, driver):
        print("normal_step")

        inputs = driver.find_element_by_id("kw")
        for keyword in word:
            inputs.send_keys(keyword)
            random_count = random.randint(1, 10)
            time.sleep(random_count / 10)
        time.sleep(random.randint(1, 2))
        su = driver.find_element_by_id("su")
        time.sleep(random.randint(0, 1))
        ActionChains(driver).click(su).perform()
        time.sleep(random.randint(1, 3))
        wait = WebDriverWait(driver, 10, 0.5)
        # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
        wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
        newurl = driver.current_url + '&si=' + 'www.kf400.cn' + "&ct=2097152"
        driver.get(newurl)
        wait = WebDriverWait(driver, 10, 0.5)
        # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
        wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
        # 找到第一个元素，看是否有保障和向下按钮
        one = driver.find_element_by_xpath("//div[@id='content_left']/div[1]")
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
                now_height = now_height + random.randint(2, 6)
                js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                driver.execute_script(js)
                time.sleep(random.randint(1, 3))
            else:
                tmp = random.randint(2, 6)
                now_height = now_height - tmp if now_height > tmp else 0
                js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(now_height)
                driver.execute_script(js)
                time.sleep(random.randint(1, 3))
        js = "document.documentElement.scrollTop=0"
        driver.execute_script(js)
        # 判断目标网站的地址需要为正好www.kf400.cn / 斜杠后面没有后缀的，判断这是第几名，就滚到【第几名 / 总位数】的位置，停留随机1~3秒.如果都是带后缀的内页就点击第一个带www.kf400.cn的目标网站
        # 获取所有带目标网站的地址

        dict1 = {}
        dict2 = {}
        all_divs = driver.find_elements_by_xpath("//div/h3")
        ad_count = all_divs.__len__()-10
        divs = driver.find_elements_by_xpath("//div[@class='result c-container new-pmd']")
        for div in divs:
            divas = div.find_elements_by_xpath(".//div//a")
            for diva in divas:
                if diva.text == "www.kf400.cn/":
                    tmp = divs.index(div)
                    dict1[tmp] = diva.text
                if "www.kf400.cn" in diva.text:
                    tmp = divs.index(div)
                    dict2[tmp] = diva.text
        if dict1.__len__() > 0:
            index = sorted(dict1.items())[0][0]
            dest = divs[index]
            js = "document.documentElement.scrollTop=document.body.scrollHeight*" + str((index + ad_count - 1)/all_divs.__len__())
            driver.execute_script(js)

            # if index==0:
            #     driver.execute_script("arguments[0].scrollIntoView();", divs[index])
            #     time.sleep(random.randint(1, 3))
            # else:
            #     driver.execute_script("arguments[0].scrollIntoView();", divs[index-1])
            #     time.sleep(random.randint(1, 3))

            random_num = random.randint(1, 100)
            # 标题
            if random_num > 20:
                index = sorted(dict1.items())[0][0]
                dest = divs[index]
                a = dest.find_element_by_xpath(".//a[1]")
                ActionChains(driver).click(a).perform()
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
                    time.sleep(random.randint(1, 3))
                else:
                    a = dest.find_element_by_xpath("./div[2]/a[1]")
                    # ActionChains(driver).move_to_element(a).perform()
                    # time.sleep(300)
                    ActionChains(driver).click(a).perform()
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
            time.sleep(random.randint(1, 3))
            random_num = random.randint(1, 100)
            # 标题
            if random_num > 20:
                index = sorted(dict2.items())[0][0]
                dest = divs[index]
                a = dest.find_element_by_xpath(".//a[1]")
                ActionChains(driver).click(a).perform()
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
                    time.sleep(random.randint(1, 3))
                else:
                    a = dest.find_element_by_xpath("./div[2]/a[1]")
                    # ActionChains(driver).move_to_element(a).perform()
                    # time.sleep(300)
                    ActionChains(driver).click(a).perform()
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
                    time.sleep(random.randint(1, 3))


def main():
    print("start __main__")
    words = ["400电话", "400电话办理"]
    thread1 = myThread(words)
    thread2 = myThread(words)
    thread3 = myThread(words)
    thread4 = myThread(words)
    thread5 = myThread(words)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    print("end __main__")


if __name__ == '__main__':
    main()
