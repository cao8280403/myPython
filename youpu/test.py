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
import requests

# url= "http://i.baidu.com/"
# cookie = {
#     "BDUSS": "w2SU81Qkc5R2FnQUpKb3VqQjhVRn5jem91Tzc3ZWVPSi1vSDJTem8zOGFGV3BjQVFBQUFBJCQAAAAAAAAAAAEAAADPPDDtuqO1wjc2c2U2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqIQlwaiEJcR2"}

# html = requests.get(url,cookies=cookie).content
# print(html)
# with open("bai.html","wb") as f:
#     f.write(html)
#     f.close()

opt = webdriver.ChromeOptions()
# opt.headless = True              # 把Chrome设置成可视化无界面模式
# opt.add_argument('--headless')
opt.add_argument('lang=zh_CN.UTF-8')
# opt.add_argument('--disable-infobars')

opt.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(options=opt)
driver.get("https://www.baidu.com/")
# input("sidh")
cookie_list = "BDUSS=w2SU81Qkc5R2FnQUpKb3VqQjhVRn5jem91Tzc3ZWVPSi1vSDJTem8zOGFGV3BjQVFBQUFBJCQAAAAAAAAAAAEAAADPPDDtuqO1wjc2c2U2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqIQlwaiEJcR2;BAIDUID=A64422BF88932C13E9351E87AFD6CE15:FG=1;PTOKEN=e439ccf53e2dcfd284c7c33071891a31;STOKEN=d23c77c353cbe0af594202d5bd18ee13a0738b261296f8a749a4dd3edcd15ecd;UBI=fi_PncwhpxZ%7ETaJc2QUP%7EvB6zL7Ycc5wn0I"
# cookie_list = driver.get_cookies()
driver.delete_all_cookies()
cookie_list_array = cookie_list.split(";")
for cookie in cookie_list_array:
    cookie_dict = {
        "domain": ".baidu.com",  # 火狐浏览器不用填写，谷歌要需要
        'name': cookie.split("=")[0],
        'value': cookie.split("=")[1],
        "expires": "",
        'path': '/',
        'httpOnly': False,
        'HostOnly': False,
        'Secure': False}
    driver.add_cookie(cookie_dict)
# driver.add_cookie({'name': 'foo', 'value': 'bar',
#                    "BDUSS": 'w2SU81Qkc5R2FnQUpKb3VqQjhVRn5jem91Tzc3ZWVPSi1vSDJTem8zOGFGV3BjQVFBQUFBJCQAAAAAAAAAAAEAAADPPDDtuqO1wjc2c2U2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqIQlwaiEJcR2'})
# driver.add_cookie(cookie)
# driver.get("http://i.baidu.com/")

driver.refresh()
# 窗口标题
print(driver.title)
# 窗口url
print(driver.current_url)

inputs = driver.find_element_by_id("kw")
inputs.send_keys("渣男")
su = driver.find_element_by_id("su")
ActionChains(driver).click(su).perform()
wait = WebDriverWait(driver, 10, 0.5)
# 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
one = driver.find_element_by_xpath("//div[@id='content_left']/div[@data-click][1]")
c_tools = one.find_elements_by_xpath(".//div[@class='c-tools']")  # 向下
