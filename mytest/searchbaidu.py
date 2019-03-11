import requests
import os
import time
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0'
}
html = 'https://www.baidu.com/'
# 需要使用url和headers生成一个Request对象，然后将其传入urlopen方法中
req = request.Request(html, headers=headers)
resp = request.urlopen(req)
content = resp.read().decode('utf-8')
f = open('baidu.html', 'w', encoding='utf-8')
f.write(content)
f.close()
