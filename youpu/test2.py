#!coding=utf-8
import time
from selenium import webdriver
import pickle
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By  # 定位器
from selenium.webdriver.common.keys import Keys  # 键盘对象
from selenium.webdriver.support import expected_conditions as EC  # 判断器
from selenium.webdriver.support.wait import WebDriverWait  # 浏览器等待对像


class BaiduSpider(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.get(url='https://www.baidu.com')
        self.set_cookie()
        self.is_login()

    def is_login(self):
        '''判断当前是否登陆'''
        self.driver.refresh()
        time.sleep(3)
        html = self.driver.page_source
        if html.find(self.username) == -1:  # 利用用户名判断是否登陆
            # 没登录 ,则手动登录
            self.login()
        else:
            # 已经登录  尝试访问搜索记录，可以正常访问
            # self.driver.get(url='http://i.baidu.com/my/history')
            # self.driver.get(url='https://www.baidu.com/')

            inputs = self.driver.find_element_by_id("kw")
            inputs.send_keys("渣男")
            su = self.driver.find_element_by_id("su")
            ActionChains(self.driver).click(su).perform()
            wait = WebDriverWait(self.driver, 10, 0.5)
            # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
            wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))
            time.sleep(30)  # 延时看效果

    def login(self):
        '''登陆'''
        time.sleep(60)  # 等待手动登录
        self.driver.refresh()
        self.save_cookie()

    def save_cookie(self):
        '''保存cookie'''
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def set_cookie(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    "domain": ".baidu.com",  # 火狐浏览器不用填写，谷歌要需要
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    BaiduSpider('_阳春白雪_', 'caoyang')  # 你的百度账号，密码