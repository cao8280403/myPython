#!/usr/bin/env python3
# analyze-dom

import sys
import json
import requests
import os
import time
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from bs4 import Doctype
from bs4 import NavigableString
from bs4 import Comment
from bs4 import Tag
import logging
logging.basicConfig(level=logging.INFO)


# 定义主流的标签，用于后面匹配
taglist = ['div', 'a', 'span', 'ul', 'img', 'li', 'table', 'th', 'td', 'script']
__cengci = 0

def getcontent(html):
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
    # 需要使用url和headers生成一个Request对象，然后将其传入urlopen方法中
    req = request.Request(html, headers=headers)
    resp = request.urlopen(req)
    content = resp.read().decode('utf-8')
    with open('rong360.html', 'w', encoding='utf_8_sig') as f:
        f.write(str(content))
        f.close()
    return content


def sum_cycle(n):
    '''
    1 to n,The sum function
    '''
    sum = 0
    for i in range(1,n + 1):
        sum += i
    return sum


def sum_recu(n):
    '''
    1 to n,The sum function
    '''
    if n > 0:
        return n + sum_recu(n - 1)#调用函数自身
    else:
        return 0


# 分析html结构，递归
def analyzedom1(content):
    logging.info('begining')
    #找到content的根节点，获取所有子节点，循环
    soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")


    body = soup.find('body')
    print(body.text)# 所有text
    print(body.parent)# 父节点
    # print(body.nextSibling)# 后一个兄弟节点
    print(body.next_sibling)# 后一个兄弟节点 没有返回None
    print(body.previous_sibling)# 前一个兄弟节点
    print(body.previous_element)#
    print(body.next_element)#
    print(body.children)# 子节点
    ch = body.contents  #获取每一个标签，其中换行算都算做一个，注释也算做一个，所以总数是标签个数x2+1

    logging.info(soup)
    return 'ok'


# 分析html结构，递归
def analyzedom(soup):
    # print(type(soup))
    if(isinstance(soup, BeautifulSoup) | isinstance(soup, Tag)):  #只解析有用的节点 tag标签
        nodes = soup.contents  # 获取每一个子节点，其中换行算都算做一个，注释也算做一个，所以总数是标签个数x2+1
        # 遍历，解析每一个子节点
        for i in nodes:
            analyzedom(i)
            print(i)
    else:
        print(soup)

    # body = soup.find('body')
    # print(body.text)# 所有text
    # print(body.parent)# 父节点
    # # print(body.nextSibling)# 后一个兄弟节点
    # print(body.next_sibling)# 后一个兄弟节点 没有返回None
    # print(body.previous_sibling)# 前一个兄弟节点
    # print(body.previous_element)#
    # print(body.next_element)#
    # print(body.children)# 子节点
    # ch = body.contents  #获取每一个标签，其中换行算都算做一个，注释也算做一个，所以总数是标签个数x2+1
    # logging.info(soup)
    return 'ok'


def main():
    # print("循环求和：",sum_cycle(100))
    # print("递归求和：",sum_recu(100))
    html = 'https://www.rong360.com/nantong/s_tp9m5t12?guarantee_type=2'
    content = getcontent(html)
    soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
    analyzedom(soup)


if __name__ == '__main__':
    main()

