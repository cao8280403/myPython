#!/usr/bin/env python3
# analyze-dom

import MySQLdb
import difflib
import sys
import json
import requests
import os
import time
import datetime
import uuid
from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from bs4 import Doctype
from bs4 import NavigableString
from bs4 import Comment
from bs4 import Tag
import logging

logging.basicConfig(level=logging.INFO)
# 打开数据库连接
db = MySQLdb.connect("120.79.117.64", "root", "123456", "internet_product_collector", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 定义主流的标签，用于后面匹配
taglist = ['div', 'a', 'span', 'ul', 'img', 'li', 'table', 'th', 'td', 'script']
totalcengci = 0
totaltext = ''


def insert_sql(node_prefix, node_brother_count, node_likely_count):
    sql = """INSERT INTO node_list(guid,
             create_time, node_prefix, node_brother_count, node_likely_brother_count,node_depth,node_img,node_to_img,node_total_depth)
             VALUES ( '%s','%s','%s','%s','%s','%s','%s','%s','%s') """
    guid = str(uuid.uuid1())
    createtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    sql = sql % (guid, createtime, node_prefix, node_brother_count, node_likely_count, 1, 1, 1, 1)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


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
    for i in range(1, n + 1):
        sum += i
    return sum


def sum_recu(n):
    '''
    1 to n,The sum function
    '''
    if n > 0:
        return n + sum_recu(n - 1)  # 调用函数自身
    else:
        return 0


# 分析html结构，获取相似节点的个数
def comparenodes(brothernodeslist, soup):
    # 遍历列表，找出相似度高的节点，计算个数
    count = 0
    for i in brothernodeslist:
        length = min(60, len(str(i)))
        substr1 = str(i)[:length]
        substr2 = str(soup)[:length]
        flag = string_similar(substr1, substr2)
        # 如果相似度大于0.8则认为是相似结构，计入兄弟个数中
        if flag > 0.8:
            count = count + 1
    count = count - 1  # 最后减去自身
    return count

    # 判定是否是img节点


def check_img(soup):
    flag = False

    return flag


# 分析html结构，递归
def analyzedom(soup):
    if str(soup).find('e5725ca4baa8e71a3f4a9ef4ce060fda25a317da') != -1:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    # print(type(soup))
    # 判定是否是img节点
    check_img(soup)
    # 寻找兄弟节点
    global totaltext
    flag = '#########################################################################################################################################################' \
           ''
    count = 0
    brothernodeslist = []  # 当前soup层级所有兄弟节点（包括自己）
    totaltext = totaltext + flag + '\n' + str(soup) + '\n'
    if (isinstance(soup, Tag)):  # 只解析有用的节点 tag标签
        parentnode = soup.parent
        nextnode = soup.next_sibling
        # 判断有多少兄弟节点跟此soup的结构相同（计算父节点contents 内容相同的个数）
        brothernodes = parentnode.contents
        for i in brothernodes:
            if (isinstance(i, BeautifulSoup) | isinstance(i, Tag)):
                brothernodeslist.append(i)
            # string_similar(i, )
    brothernodescount = brothernodeslist.__len__() - 1  # 兄弟节点个数
    # 结构相似的兄弟节点个数
    likenodecount = comparenodes(brothernodeslist, soup)
    length = min(60, len(str(soup)))
    node_prefix = str(soup)[:length]
    insert_sql(node_prefix, brothernodescount, likenodecount)
    if (isinstance(soup, BeautifulSoup) | isinstance(soup, Tag)):  # 只解析有用的节点 tag标签
        # if (soup.string == None):  # 如果有多个子节点，返回null
        nodes = soup.contents  # 获取每一个子节点，其中换行算都算做一个，注释也算做一个，所以总数是标签个数x2+1
        if len(nodes) != 0 :
            # 遍历，解析每一个子节点
            for i in nodes:
                if (isinstance(i, BeautifulSoup) | isinstance(i, Tag)):
                    analyzedom(i)
                # else:
                #     print(str(i))
                    # return
        else:  # 如果有一个子节点，返回内容
            print('我是一个叶子节点')
        # else:
        #     print(str(soup))
        # return
    return 'ok'


def main():
    # print("循环求和：",sum_cycle(100))
    # print("递归求和：",sum_recu(100))
    html = 'https://www.rong360.com/nantong/s_tp9m5t12?guarantee_type=2'
    content = getcontent(html)
    soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
    body = soup.find('body')
    fo = open('temp.text', 'w', encoding='utf_8_sig')
    analyzedom(body)
    fo.write(totaltext)
    fo.close()


if __name__ == '__main__':
    main()
    # 关闭数据库连接
    db.close()
