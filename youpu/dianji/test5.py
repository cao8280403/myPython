# coding=utf-8
from selenium import webdriver
from public import *
# from pymouse import PyMouse键盘对象
from selenium.webdriver.support import expected_conditions as EC  # 判断器
from selenium.webdriver.support.wait import WebDriverWait  # 浏览器等待对像
from selenium.webdriver.common.by import By  # 定位器
import time, requests
import traceback
import pyautogui
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
print(time.strftime("%Y-%m-%d %H:%M:%S"))
time1 = time.time()
time.sleep(3.12)
time2 = time.time()
print(round(time2-time1))

options = webdriver.ChromeOptions()  # 设置代理
# options.add_argument("--user-data-dir="+r"C:/Users/Caoyang/AppData/Local/Google/Chrome/User Data/")
# extension_path = "C:/Users/Caoyang/AppData/Local/Google/Chrome/User Data/Default/Extensions/eiimnmioipafcokbfikbljfdeojpcgbh/4.5.0.1_0.crx"
# options.add_extension(extension_path)
# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)
# --host-rules=MAP xxx.xxx.com 127.0.0.1,MAP xxx.xxx.com 127.0.0.1
# options.add_argument('--host-resolver-rules=MAP www.kf400.cn 127.0.0.1')
# options.add_argument("--proxy-server=http://222.186.180.95:40243")
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示正在受自动化软件控制#跟上面只能选一个
options.add_argument("disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹
options.add_argument("disable-cache")  # 禁用缓存
options.add_argument('--disk-cache-dir=e:\chromecahce')
# 启动浏览器，并设置好wait
browser = webdriver.Chrome(options=options)
# browser.set_page_load_timeout(1)


try:
    browser.get("http://www.baidu.cn/")
    inputs = browser.find_element_by_id("kw")
    # inputs.send_keys("www.goldyuesao.cn")
    inputs.send_keys("www.kf400.cn")
    su = browser.find_element_by_id("su")
    ActionChains(browser).click(su).perform()
    time.sleep(1)
    one = browser.find_element_by_xpath("//div[@id='content_left']/div[@data-click][1]")
    a1 = one.find_element_by_xpath(".//a[1]")

    ActionChains(browser).click(a1).perform()
    # time.sleep(3)
    windows = browser.window_handles
    # t1 = time.time()
    browser.switch_to.window(windows[-1])
    t2 = time.time()
    # print(t2-t1)
    time.sleep(2)
    browser.execute_script("window.open();")
    # browser.close()
    t3 = time.time()
    print(t3-t2)
    # browser.get('chrome://settings/clearBrowserData')
    # browser.switch_to.window(windows[-1])
    # sda = browser.find_element_by_id("clearBrowsingDataConfirm")
    # time.sleep(30)
    # for i in range(7):
    #     time.sleep(1)
    #     pyautogui.press('tab')
    # pyautogui.press('enter')
    # sda = browser.find_elements_by_xpath("//cr-button[@id='clearBrowsingDataConfirm']")
    # ActionChains(browser).click(sda).perform()
    # wait = WebDriverWait(browser, 3, 0.5)
    # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
    # wait.until(EC.presence_of_all_elements_located((By.ID, "website")))
    # element = WebDriverWait(browser, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, '/html')))
    # element = WebDriverWait(browser, 3, 0.1).until(EC.presence_of_element_located((By.ID, "div_company_mini")))
    # browser.close()
    # ActionChains(browser).send_keys(Keys.CONTROL + "t").perform()
    # browser.find_element_by_xpath("").sendKeys(Keys.CONTROL + "t")
    # browser.execute_script("window.open();")
    # windows = browser.window_handles
    # browser.switch_to.window(windows[-1])
    # browser.switch_to.window(windows[1])
    # browser.close()
    # for m in range(20):
    #     time.sleep(0.1)
    #     title=browser.title
    #     print( str(m)+ title)
    #     browser.quit()
except Exception as err:        # 捕获timeout异常
    print('traceback.print_exc():' + str(traceback.print_exc()))
    browser.execute_script('window.stop()')
finally:
    print(11)
    browser.quit()
