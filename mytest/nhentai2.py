import json

import requests
import os
import time
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0'
}
html = 'https://nhentai.net/g/252398/'
# 需要使用url和headers生成一个Request对象，然后将其传入urlopen方法中
req = request.Request(html, headers=headers)
resp = request.urlopen(req)
content = resp.read().decode('utf-8')
f = open('caifuchaoshi.html', 'w', encoding='utf-8')
f.write(content)
f.close()
os.makedirs('pic/')
soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
link_node1 = soup.find('div', class_="content")
link_node3 = soup.find('div', id='thumbnail-container')
link_node2 = soup.find_all('div', class_="thumb-container")
link_node4 = soup.find_all('a', class_="gallerythumb")

'''
搜索的是小图片
for i in link_node2:
    m = i.find('noscript')
    p = m.find('img')
    pic_link = p.get('src')  # 拿到图片的具体 url
    # pic_link = 'https://'+pic_link
    print(pic_link)
    print(pic_link.split('/')[-1])
    # print(link_node2.name, link_node2['href'], link_node2['class'], link_node2.get_text())
    #     create_dir('pic/')
    r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
    with open('pic/{}'.format(pic_link.split('/')[-1]), 'wb') as fi:
        fi.write(r.content)
'''
for i in link_node4:
    bb = 'https://nhentai.net'+i['href']
    req = request.Request(bb, headers=headers)
    resp = request.urlopen(req)
    content = resp.read().decode('utf-8')
    soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
    a1 = soup.find('div',class_='container')
    a2 = a1.find('img')
    a3 = a2['src']
    r = requests.get(a3, headers=headers)  # 下载图片，之后保存到文件
    with open('pic/{}'.format(a3.split('/')[-1]), 'wb') as fi:
        fi.write(r.content)


