# coding: utf-8

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
import pyautogui


# pyautogui.moveTo(1, 1, duration=1)
# 创建一个谷歌浏览器对象


# 屏幕分辨率设置
def setDisplay():
    display_size = [
        [1920, 1080],
        [1680, 1050],
        [1600, 900],
        [1440, 900],
        [1400, 1050]
    ]
    d_size = random.choice(display_size)

    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsWidth = d_size[0]
    dm.PelsHeight = d_size[1]
    dm.BitsPerPel = 32
    dm.DisplayFixedOutput = 0
    win32api.ChangeDisplaySettings(dm, 0)


# setDisplay()

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.baidu.com")

# time.sleep(30)
# options = webdriver.ChromeOptions()
# options.binary_location = r'C:\Users\Secoo\AppData\Roaming\360se6\Application\360se.exe'
# browser = webdriver.Chrome(r'D:\chromedriver.exe', options=options)
# cookie = driver.get_cookies()
# cookie_path = 'cookie.txt'

ac = ActionChains(driver)
# cookies = "BDUSS=FCMGRCZEh5Y1lCZ3R5Mk82dnhTV3ZmNGswfmxxZ0tUNHdVY0J0aVJ6VElGR3BjQVFBQUFBJCQAAAAAAAAAAAEAAAD8kjDtuqO1wjc4ZmEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMiHQlzIh0JcR0;BAIDUID=D649F01952DC4EEC78735E7D582F59F6:FG=1;PTOKEN=ccc1d9c7b5335dd7f22fb8c2d924073c;STOKEN=e9f2b24ea96095c25c093e5d83f44ef9f937a4632eb38a9a02d6cf422fedfb21;UBI=fi_PncwhpxZ%7ETaJc7bQ-GLORVjOYXHTjLvR"
# cookies = "PSTM=1594432774; BAIDUID=56B6387D07533AACFEBC69487E660D29:FG=1; BIDUPSID=FC43B94AB543C8E292A6C1D8C3CCFADF; BD_UPN=12314753; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=7g8OJexroG3SYzrrvW_aUtUoreKKvV3TDYLEHSzb941gvRIVNZ5hEG0PtoaGdu_-ox8EogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJu8_CthJKvJHJ-kh4oMbt_ybeT22-usbeoJ2hcH0KLKbfnTb4T8K6F8DnJP-pQdMDvOBlQs-fb1MRjvehnbQRDPyH5GajvR3b5noh5TtUJoeCnTDMRhqfk1MMjyKMniBnr9-pnE0hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuDT0BjT3BDGus24cQb4_8VI5bM6rjDnCrQn0VXUI8LNDHtTtfbN4tQt3LKRvlfM53bPb1-xTXjJO7ttoy3DrTbtJT5nOAqqTTDxoh-xL1Db3pKjvMtg3t3tovL-OoepvoX55c3MkDLPjdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjKjLEtJ-toDIXJKL3fP36q4TM2tFqMfLX5-RLf2uHLp7F5l8-h45Y-4OP-RDj3a3pb4vCW65LaK5HBMjxOKQm04bkKlLV5HO9BqojMNCeWC3N3KJmOMK9bT3v5tDQ2-R32-biW2tH2MbdalOP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe6LbejOWjHDs5JtXKD600PK8Kb7VbnARLUnkbJkXhPteQhcE-jrq-MA-Q4blDPoNyUR-36t7Qbrr0xRfyNReQIO13hcdSlrLjt7pQT8r5MnK0-3tX-jyXInNab3vOIJTXpO1jxPzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_ffR4f_CLQKbRofJ-k5-o_-PLH52T22-usJKkO2hcHMPoosIObWJ6KKRKiBUQP-pQy-DTia-QCtMbUoqRHyhb0-6c3DfJqQfcpBHLtBp5TtUJMDnjjbborqt4be-oyKMnitIv9-pPKWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHjo0eH-O3e; delPer=0; BD_CK_SAM=1; PSINO=5; BD_HOME=1; sug=3; sugstore=0; ORIGIN=0; bdime=0; BAIDUID_BFESS=56B6387D07533AACFEBC69487E660D29:FG=1; COOKIE_SESSION=1039_0_6_9_4_6_0_0_6_5_0_2_3_0_0_0_1607158619_0_1607220373%7C9%23430763_15_1604303863%7C9; H_PS_PSSID=1441_33123_33061_33099_33101_32938_26350_33198_33148_22159; H_PS_645EC=ba63A%2B3peqIyAquzIMrN4GKROY4FenRAWLIFfv6bryssk8esHSTPYikrRI8; BA_HECTOR=a0218l2120058h2kae1fsofau0r; BDSVRTM=0"
cookie = {}

try:
    # 浏览器对象打开百度地址
    driver.get("https://www.baidu.com")

    # newwindow = 'window.open("https://www.baidu.com");'

    driver.delete_all_cookies()
    # aaabb = driver.get_cookies()
    # for line in cookies.split(';'):
    #     key, value = line.split('=', 1)  # 1代表只分一次，得到两个数据
    #     cookie[key] = value
    # cookie["name"] = "BA_HECTOR"
    # cookie["value"] = "2o0k80a0a18h2165fb1fsof9i0q"
    # print(cookie)

    # driver.add_cookie(cookie)
    # driver.execute_script(newwindow)
    #
    # input("查看效果")
    # aaa = driver.get_cookies()
    # time.sleep(3)
    # # driver.refresh()
    # driver.get("https://www.baidu.com")
    # aaabb = driver.get_cookies()
    # driver.refresh()

    # time.sleep(3)
    # 查找id为 'kw'的标签，即输入框
    inputs = driver.find_element_by_id("kw")
    # 在输入框中填入'Python'
    site = "www.kf400.cn"
    word = "400电话"
    inputs.send_keys(word)
    # '按下'回车键（第一种）
    inputs.send_keys(Keys.ENTER)
    # 点击'百度一下'（第二种）
    # browser.find_element_by_id("su").click()
    # 创建一个等待对像，超时时间为10秒，调用的时间间隔为0.5
    wait = WebDriverWait(driver, 5, 0.5)

    # 每隔0.5秒检查一次，直到页面元素出现id为'content_left'的标签
    wait.until(EC.presence_of_all_elements_located((By.ID, "content_left")))

    all_divs = driver.find_elements_by_xpath("//div/h3")



    for i in range(10):
        js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(i)
        driver.execute_script(js)
        time.sleep(2)  # 休眠
        js2 = "document.documentElement.scrollTop=document.body.scrollHeight/7*" + str(i)
        driver.execute_script(js2)
        time.sleep(2)  # 休眠

    # driver.switchTo().fame("id")
    # driver.switchTo().fame("")
    # driver.switchTo().fame("selector")
    # hold = driver.find_element_by_id('su')
    # slider = driver.find_element_by_xpath("//div[@id='content_left']/div[1]/a")
    # ac.click_and_hold(hold).perform()
    # ac = ActionChains(driver)
    # one = driver.find_element_by_xpath("//div[@id='content_left']/div[1]")
    #
    # c_tools = one.find_elements_by_xpath(".//div[@class='c-tools']")
    # data_baobiao = one.find_elements_by_xpath(".//a[@data-baobiao]")
    # data_bao = one.find_elements_by_xpath(".//span[@data-bao]")
    # if len(data_baobiao) > 0:
    #     baobiao = data_baobiao[0]
    #     ac.move_to_element(baobiao).perform()
    # if len(data_bao) > 0:
    #     bao = data_bao[0]
    #     ac.move_to_element(bao).perform()
    # time.sleep(20)
    # if len(c_tools) > 0:
    #     xiangxia = c_tools[0]
    #     ac.move_to_element(xiangxia).perform()

    dict1 = {}
    dict2 = {}
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
        driver.execute_script("arguments[0].scrollIntoView();", dest)
        time.sleep(2)
        random_num = random.randint(1, 100)
        # 标题
        if random_num > 20:
            index = sorted(dict1.items())[0][0]
            dest = divs[index]
            a = dest.find_element_by_xpath(".//a[1]")
            ActionChains(driver).click(dest).perform()
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
            else:
                a = dest.find_element_by_xpath("./div[2]/a[1]")
                # ActionChains(driver).move_to_element(a).perform()
                # time.sleep(300)
                ActionChains(driver).click(a).perform()

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



    elif dict2.__len__() > 0:
        index = sorted(dict2.items())[0][0]
        dest = divs[index]
        driver.execute_script("arguments[0].scrollIntoView();", dest)
        time.sleep(200)

    time.sleep(100)
    one = driver.find_element_by_xpath("//div[@id='content_left']/div[1]//a[1]")
    # one = divs.find_element_by_xpath("./div[1]//a[1]")
    # ac.move_to_element(one).perform()
    # ac.click_and_hold(one).perform()
    ac.click(one).perform()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])  # 切换到新窗口
    print(driver.window_handles)  # 查看所有window handles
    driver.close()
    # driver.find_element_by_class_name("s_tab_inner")
    # slider = driver.find_element_by_id("content_left")
    # for y in range(6):
    #     y = y * 103
    #     print(y)
    #     ac.move_to_element_with_offset(slider, 0,y).perform()
    #     ac = ActionChains(driver)  # 新建操作，不然会重复
    #     time.sleep(0.5)
    #

    time.sleep(3)
    # ac.move_to_element('slider').perform()
    # time.sleep(3)
    # # ac.drag_and_drop_by_offset(slider, 1000, 0).perform()
    # time.sleep(3)
    # button = driver.find_elements_by_class_name('over')
    # ac.move_to_element('button').perform()  # 移动 点击执行
except Exception as e:
    print(e)
else:
    # 打印请求的url
    print(driver.current_url)
    # 打印所有cookies
    print(driver.get_cookies())

    newurl = driver.current_url + '&si=' + site + "&ct=2097152"
    driver.get(newurl)

finally:
    # 等待10秒
    time.sleep(4)
    # 关闭浏览器对象
    driver.close()
