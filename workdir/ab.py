import time
from numba import jit
#
# @jit
# def num():
#
#     arr = []
#     for i in range(10000000):
#         arr.append(i)
#
#
# stime = time.time()
# num()
# etime = time.time() - stime
# # print(arr)
# print('用时:{}秒'.format(etime))
# import newspaper
#
# sina=newspaper.Article("https://news.sina.com.cn/gov/xlxw/2020-02-07/doc-iimxxste9531083.shtml")
# sina.download()
# print(sina.title)
# print(sina.text[:150])
# print(sina.doc)
# print(sina.authors)
# print(sina.html)

# from newspaper import Article
# # 目标新闻网址
# url = 'https://www.jihaoba.com/news/show/7632'
# news = Article(url, language='zh')
# news.download()        # 加载网页
# news.parse()           # 解析网页
# print('题目：',news.title)       # 新闻题目
# print('正文：\n',news.text)      # 正文内容
# print(news.authors)     # 新闻作者
# print(news.keywords)    # 新闻关键词
# print(news.summary)     # 新闻摘要

# from newspaper import Article
#
# article = Article('https://money.163.com/19/1130/08/EV7HD86300258105.html')
# article.download()
# article.parse()
# print("title=", article.title)
# print("author=", article.authors)
# print("publish_date=", article.publish_date)
# print("top_iamge=", article.top_image)
# print("movies=", article.movies)
# print("text=", article.text)
# print("summary=", article.summary)


import math

print("PI=%f" % math.pi)