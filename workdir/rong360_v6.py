#!/usr/bin/env python3
# analyze-dom

import MySQLdb
import difflib
import sys
import json
import requests
import chardet
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
from selenium import webdriver
import time

logging.basicConfig(level=logging.INFO)
# 打开数据库连接
db = MySQLdb.connect("120.79.117.64", "root", "123456", "internet_product_collector", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# html = 'https://www.rong360.com/nantong/s_tp9m5t12?guarantee_type=2'
# html = 'http://www.caiqi.com/'
# html = 'https://www.p2peye.com/'
# html = 'http://licai.jd.com/?from=jrad_950119&loc=2'
# html = 'https://jr.mi.com/finance.html'
html = 'http://www.jinrongchaoshi.com/'
# html = 'http://www.fminers.com/Home/Plan/financial.html'
# html = 'http://www.xfkou.com/bank.html'
# html = 'http://trust.xfkou.com/'
# 定义主流的标签，用于后面匹配
strlist = ['收益率', '年化', '%', '起息', '标的', '金额', '收益', '期限', '元', '万', '起投', '月供', '利息', '抵押', '流水', '社保', '平台', '.']
numlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '一', '二', '三', '四', '五', '六', '七', '八', '九']
totalcengci = 0
totaltext = ''
yezicount = 0
cengshulist = []


def insert_sql(node_prefix, node_brother_count, node_likely_count, imgcount, julilist, cengshu, nodepath, brother_sort,
               totalstrcount, strcount, numcount, isproduct):
    sql = """INSERT INTO node_list412(guid,
             create_time, website, node_prefix, node_brother_count, node_likely_brother_count,node_depth,node_img,node_to_img,node_total_depth,nodepath,isproduct, node_brother_sort,totalstrcount,strcountdict,numcountdict)
             VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    guid = str(uuid.uuid1())
    createtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # sql = sql % (guid, createtime, node_prefix, node_brother_count, node_likely_count, 1, 1, 1, 1)
    try:
        # 执行sql语句,这种写法防止注入
        cursor.execute(sql, (
            guid, createtime, html, node_prefix, node_brother_count, node_likely_count, cengshu, imgcount, julilist, 1,
            nodepath, isproduct, brother_sort, totalstrcount, str(strcount), str(numcount)))
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(str(e))
        # Rollback in case there is any error
        db.rollback()


def setmaxcengshu(maxcengshu):
    sql = """UPDATE node_list412 SET node_total_depth = %s where website = %s """
    try:
        # 执行sql语句,这种写法防止注入
        cursor.execute(sql, (maxcengshu, html))
        # 提交到数据库执行
        db.commit()
    except Exception:
        print(Exception)
        # Rollback in case there is any error
        db.rollback()


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def getcontent():
    driver = webdriver.Chrome()  # 初始化一个浏览器实例：driver  exe文件放到python安装根目录下
    time.sleep(5)  # 暂停10秒钟,时间太短会出错
    driver.get(html)  # 通过get()方法，打开一个url站点
    driver.maximize_window()
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    for i in range(10):
        js = "document.documentElement.scrollTop=document.body.scrollHeight/10*" + str(i)
        driver.execute_script(js)
        time.sleep(1)  # 休眠2秒
    content = driver.page_source
    # print(content)
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


# 分析html结构，获取关键字的匹配List
def getstrdict(soupstr):
    # soupstr = str(soup)
    global strlist
    dict = {}
    for j in strlist:
        count = 0
        for i in range(len(soupstr) - 1):
            if soupstr[i:i + len(j)] == j:
                count += 1
        dict[j] = count
    return dict


# 分析html结构，获取数字的匹配List
def getnumdict(soupstr):
    # soupstr = str(soup)
    global numlist
    dict = {}
    for j in numlist:
        count = 0
        for i in range(len(soupstr) - 1):
            if soupstr[i:i + len(j)] == j:
                count += 1
        dict[j] = count
    return dict


# 分析html结构，递归
def analyzedom(soup):
    totalstrcount = ''  # 叶子节点总字符数
    strcount = ''  # 叶子节点关键字总数
    numcount = ''  # 叶子节点数字总数
    # appendstr = ''  # 叶子节点字符串拼接
    totalstr = ''  # 此节点的总共的的叶子节点的总字符
    tempsoup = ''  # 此节点返回的值，是叶子节点的时候就返回值，不是叶子则返回空串
    # 寻找兄弟节点
    # global totaltext, yezicount
    # flag = '#########################################################################################################################################################' \
    #        ''
    count = 0
    brothernodeslist = []  # 当前soup层级所有兄弟节点（包括自己）
    # totaltext = totaltext + flag + '\n' + str(soup) + '\n'
    # 判断是否有img标签,并计算距离层数
    hasimg = 0
    juli = 0
    '''
    img = soup.find('img')
    if isinstance(img, Tag):
        hasimg = 1
        # global juli
        juli = 1
        imgparent = img.parent
        while imgparent != soup:
            imgparent = imgparent.parent
            juli = juli + 1
    '''
    julilist = []
    pingjunshu = 0.0
    imgs = soup.find_all('img')
    imgcount = len(imgs)
    if imgcount > 0:
        hasimg = 1
        for img in imgs:
            if isinstance(img, Tag):
                juli = 1
                imgparent = img.parent
                while imgparent != soup:
                    imgparent = imgparent.parent
                    juli = juli + 1
                # if len(img.contents) != 0:
                #     juli = juli/(juli+1)
                # else:
                #     juli = 1
                julilist.append(juli)
        # juli = sum(julilist)/len(imgs)

    # 统计此节点所在层数
    cengshu = 1
    nodepath = "<" + soup.name + ">"
    tempparent = soup.parent
    while not str(tempparent).startswith('<html'):
        nodepath = "<" + tempparent.name + ">" + nodepath
        tempparent = tempparent.parent
        cengshu = cengshu + 1
    # print(nodepath)
    cengshulist.append(cengshu)
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

    if (isinstance(soup, BeautifulSoup) | isinstance(soup, Tag)):  # 只解析有用的节点 tag标签
        # if (soup.string == None):  # 如果有多个子节点，返回null
        nodes = soup.contents  # 获取每一个子节点，其中换行算都算做一个，注释也算做一个，所以总数是标签个数x2+1
        if len(nodes) != 0:
            # 遍历，解析每一个子节点
            for i in nodes:
                # if (isinstance(i, BeautifulSoup) or isinstance(i, Tag)):
                totalstr = totalstr + analyzedom(i)
    else:  #不是Tag标签可能就是叶子节点
        # yezicount = yezicount + 1
        tempsoup = soup.replace(' ', '')
        tempsoup = tempsoup.replace('\n', '')
        # if len(tempsoup) > 0 and len(tempsoup) < 40:
        #      appendstr = appendstr + tempsoup
        # else:  # 如果有一个子节点，返回内容
        # print(soup.text)

        # else:
        #     print(str(soup))
        # return
    # 如果存在相似结构的兄弟节点，则判断此soup的关键字个数，数字个数和总字符数

    # if (likenodecount > 0):
    #     print(appendstr)
    #     totalstrcount = len(appendstr)
    #     strcount = getstrdict(appendstr)
    #     numcount = getnumdict(appendstr)
    brother_sort = brothernodeslist.index(soup) + 1
    length = min(60, len(str(soup)))
    node_prefix = str(soup)[:length]
    # if len(totalstr)>0:
    #     print(node_prefix,end='')
    print(totalstr,end='')
    print(tempsoup)
    # insert_sql(node_prefix, brothernodescount, likenodecount, imgcount, str(julilist), cengshu, nodepath, brother_sort,
    #            totalstrcount, strcount, numcount, "0")

    return tempsoup


def main():
    # print("循环求和：",sum_cycle(100))
    # print("递归求和：",sum_recu(100))
    content = getcontent()
    soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
    body = soup.find('body')
    # fo = open('temp.text', 'w', encoding='utf_8_sig')
    analyzedom(body)
    # print(yezicount)
    print(max(cengshulist))
    setmaxcengshu(max(cengshulist))
    # fo.write(totaltext)
    # fo.close()


if __name__ == '__main__':
    main()
    # 关闭数据库连接
    db.close()
