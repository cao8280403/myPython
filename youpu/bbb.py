from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep

filters = ['招聘', '诚聘', '社招']
contents = [
    '独自等待安全团队诚聘, https://www.jb51.net/',
    '独自等待安全团队招聘, https://www.jb51.net/',
    '独自等待安全团队社招, https://www.jb51.net/',
    '独自等待信息安全博客, https://www.jb51.net/',
]

for content in contents:
    if any(keyword in content for keyword in filters): continue
    print(content)


abc = "abc"

mmm = "abcde"
var = abc in mmm
print(var)
#
# get_12306 = webdriver.Chrome()
# get_12306.get('https://www.12306.cn/index/index.html')
#
# g_href = get_12306.find_element_by_xpath('//*[@id="J-index"]/a')
# Action = ActionChains(get_12306)
#
#
# for x in range(9):
#     x = x * 145
#     print(x)
#     Action.move_to_element_with_offset(g_href, x, 0).perform()
#     sleep(0.5)
#
# sleep(2)
#
# get_12306.quit()