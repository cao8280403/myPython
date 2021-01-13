# coding=utf-8
from selenium import webdriver
from public import *
# from pymouse import PyMouse键盘对象
from selenium.webdriver.support import expected_conditions as EC  # 判断器
from selenium.webdriver.support.wait import WebDriverWait  # 浏览器等待对像
from selenium.webdriver.common.by import By  # 定位器
import time,requests
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()  # 设置代理
# options.add_argument("--user-data-dir="+r"C:/Users/Caoyang/AppData/Local/Google/Chrome/User Data/")
# extension_path = "C:/Users/Caoyang/AppData/Local/Google/Chrome/User Data/Default/Extensions/eiimnmioipafcokbfikbljfdeojpcgbh/4.5.0.1_0.crx"
# options.add_extension(extension_path)

# 启动浏览器，并设置好wait
# browser = webdriver.Chrome(options=options)

url = 'http://www.goldyuesao.cn/'
# r =requests.get(url)
# print(r)
# print(r.text)
# print(r.content)
proxies = {'http':'http://222.186.180.87:44060'}
response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=3)
print(response.text)
r = requests.get(url, proxies=proxies, timeout=3)
print(r)
r = requests.get(url+ "/www.zip", proxies=proxies, timeout=3)
print(r)
r = requests.get(url+ "/www.zip", proxies=proxies, timeout=3)
print(r)
r = requests.get(url, proxies=proxies, timeout=3)
print(r)

# browser.get("http://www.trust400.com/")
# browser.get("http://www.goldyuesao.cn/")
# browser.execute_script("window.location.href=\"http://www.baidu.com\"")

# browser.set_page_load_timeout(1)

# try:
#     browser.get("http://www.baidu.cn/")
#     inputs = browser.find_element_by_id("kw")
#     inputs.send_keys("keyword")
#     su = browser.find_element_by_id("su")
#     time.sleep(3)
#     ActionChains(browser).click(su).perform()
#     # time.sleep(1)
#     # wait = WebDriverWait(browser, 1, 0.5)
#     # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
#     # wait.until(EC.presence_of_all_elements_located((By.ID, "website")))
#     element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body')))
#     # element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, "website")))
#     browser.execute_script("window.stop();")
#     # for m in range(20):
#     #     time.sleep(0.1)
#     #     title=browser.title
#     #     print( str(m)+ title)
#     #     browser.quit()
#
# finally:
#     print(11)
#     browser.quit()