#!/usr/bin/python3
from selenium import webdriver  # 浏览器驱动器
from selenium.webdriver.common.by import By  # 定位器
from selenium.webdriver.common.keys import Keys  # 键盘对象
from selenium.webdriver.support import expected_conditions as EC  # 判断器
from selenium.webdriver.support.wait import WebDriverWait  # 浏览器等待对像
import threading
import time
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
exitFlag = 0

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        abc(self.name, self.counter, 9)
        print("退出线程：" + self.name)






def abc(threadName, delay, counter):
    driver = webdriver.Chrome()
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--load-images=no'])
    ac = ActionChains(driver)
    driver.get("https://www.baidu.com")
    inputs = driver.find_element_by_id("kw")
    # 在输入框中填入'Python'
    site = "www.kf400.cn"
    word = "400电话"
    inputs.send_keys('4')
    # time.sleep(1)
    inputs.send_keys('0')
    inputs.send_keys('0')
    # time.sleep(1)
    inputs.send_keys('电话')
    # '按下'回车键（第一种）
    inputs.send_keys(Keys.ENTER)
    # 点击'百度一下'（第二种）
    # browser.find_element_by_id("su").click()
    # 创建一个等待对像，超时时间为10秒，调用的时间间隔为0.5
    wait = WebDriverWait(driver, 5, 0.5)

    # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
    wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
    hold = driver.find_element_by_id('su')
    # slider = driver.find_element_by_xpath("//div[@id='content_left']/div[1]/a")
    ac.click_and_hold(hold).perform()
    # ac = ActionChains(driver)
    divs = driver.find_element_by_xpath("//div[@id='content_left']")
    one = divs.find_element_by_xpath("./div[1]//a[1]")
    # ac.click_and_hold(one).perform()
    ac.click(one).perform()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])  # 切换到新窗口
    print(driver.window_handles)  # 查看所有window handles
    time.sleep(3)
    time.sleep(delay)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
thread3 = myThread(3, "Thread-2", 3)
thread4 = myThread(4, "Thread-2", 4)
thread5 = myThread(5, "Thread-2", 5)
thread6 = myThread(6, "Thread-2", 6)
thread7 = myThread(7, "Thread-2", 7)
thread8 = myThread(8, "Thread-2", 8)
thread9 = myThread(9, "Thread-2", 9)

# 开启新线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
print("退出主线程")
