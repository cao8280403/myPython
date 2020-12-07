import json
import requests
import os
import time
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup

headers = {
        # 'Host': 'www.lagou.com',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '23',
        # 'Origin': 'https://www.lagou.com',
        # 'X-Anit-Forge-Code': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'X-Anit-Forge-Token': 'None',
        # 'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
html = 'http://www.0755400.cn/news/5820.html'
# 需要使用url和headers生成一个Request对象，然后将其传入urlopen方法中
req = request.Request(html, headers=headers)
resp = request.urlopen(req)
content = resp.read().decode('utf-8')
with open('rong360.html', 'w',encoding='utf_8_sig') as f:
    f.write(str(content))
    f.close()


cengci_count = 0
soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
cengci_count += 1
body = soup.find('body')
cengci_count += 1
mainpart = body.find('div',class_='main-part')
cengci_count += 1
mainsearchmain = mainpart.find('div',class_='wrap-base main-search-main')
cengci_count += 1
wrapbaseinner = mainsearchmain.find('div',class_='wrap-base-inner wrap-clear')
cengci_count += 1
wrapmain = wrapbaseinner.find('div',class_='wrap-main')
cengci_count += 1
newlist = wrapmain.find('div',class_='wrap-main-inner new-list')
cengci_count += 1
resultpage = newlist.find('div',id='result_page')
cengci_count += 1
result = resultpage.find('div',class_='result')
cengci_count += 1
search_list = result.find('ul',class_='a-product_list search_list')
cengci_count += 1
list = search_list.find_all('li',class_='item')
cengci_count += 1
imgcengcicount = 0
for i in list:
    item_cont = i.find('div', class_='item_cont')
    imgcengcicount += 1
    bank_icon = item_cont.find('div', class_='bank_icon')
    imgcengcicount += 1
    img = bank_icon.find('img')
    imgcengcicount += 1
    print(img['src'],img['title'],img['alt'])
qq = len(list)
imgcengcicount = imgcengcicount/len(list)
cengci_count += imgcengcicount
#解析前后兄弟文档结构

# 标记层次，总层次
print('总层次'+str(cengci_count))
print('标记层次'+str(cengci_count-imgcengcicount))
# 是否含有img，与img差几层
print('与img差几层'+str(imgcengcicount))