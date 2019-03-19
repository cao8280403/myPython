import json

import requests
import os
import time
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup


def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    return r.text


def get_pic_list(html):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # 需要使用url和headers生成一个Request对象，然后将其传入urlopen方法中
    req = request.Request(html, headers=headers)
    resp = request.urlopen(req)
    content = resp.read().decode('utf-8')
    f = open('caifuchaoshi.html', 'w', encoding='utf-8')
    f.write(content)
    f.close()
    soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
    link_node1 = soup.find('div', class_="container index-container")
    link_node2 = soup.find_all('a', class_="cover")
    for i in link_node2:
        m = i.find('noscript')
        p = m.find('img')
        pic_link = p.get('src')  # 拿到图片的具体 url
        # pic_link = 'https://'+pic_link
        print(pic_link)
        print(pic_link.split('/')[-2])
    # print(link_node2.name, link_node2['href'], link_node2['class'], link_node2.get_text())
    #     create_dir('pic/')
        r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
        with open('pic/{}'.format(pic_link.split('/')[-2]+'.jpg'), 'wb') as fi:
            fi.write(r.content)
    print('over')
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find('div', id='content')
    b = a.find_all('div')
    pic_list = soup.find_all('div', class_='thumb-container')
    create_dir('pic/')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    for i in pic_list:
        p = i.find('img')
        pic_link = p.get('src')  # 拿到图片的具体 url
        print(pic_link)
        r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
        with open('pic/{}'.format(pic_link.split('/')[-1]), 'wb') as f:
            f.write(r.content)
            # time.sleep(1)  # 休息一下，不要给网站太大压力，避免被封
    # pic_list = soup.find_all('div', class_='container').find_all('section',id_='image-container')
    # for i in pic_list:
    #     a_tag = i.find('section', class_='fit-horizontal full-height').find('img')
    #     link = a_tag.get('src')
    #     # text = a_tag.get_text()
    #     get_pic(link)


def get_pic(link):
    '''
    获取当前页面的图片,并保存
    '''
    html = download_page(link)  # 下载界面
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find_all('img')  # 找到界面所有图片
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    create_dir('pic/')
    # create_dir('pic/{}'.format(link))
    for i in pic_list:
        pic_link = i.get('src')  # 拿到图片的具体 url
        r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
        with open('pic/{}'.format( pic_link.split('/')[-1]), 'wb') as f:
            f.write(r.content)
            # time.sleep(1)  # 休息一下，不要给网站太大压力，避免被封


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url):
    # page_html = download_page(url)
    get_pic_list(url)


def main():
    create_dir('pic')
    queue = [i for i in range(1, 72)]  # 构造 url 链接 页码。

    url = ''
    execute(url)

if __name__ == '__main__':
    main()
