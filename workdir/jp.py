from urllib import request

# from jparser import PageModel
# # html = urllib2.urlopen("http://news.sohu.com/20170512/n492734045.shtml").read().decode('gb18030')
import newspaper

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
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}
# html = 'http://www.0755400.cn/news/5820.html'
# req = request.Request(html, headers=headers)
# resp = request.urlopen(req)
# content = resp.read().decode('utf-8')
# pm = PageModel(content)
# result = pm.extract()
#
# print("==title==")
# print(result['title'])
# print("==content==")
# for x in result['content']:
#     if x['type'] == 'text':
#         print(x['data'])
#     if x['type'] == 'image':
#         print("[IMAGE]", x['data']['src'])
from newspaper import Article
import time
import requests

url = 'https://finance.sina.com.cn/roll/2019-06-12/doc-ihvhiqay5022316.shtml'
# baidu_url = requests.get(url=url, headers=headers, allow_redirects=False)
# var = baidu_url.headers['Location']
ticks = time.time()
a = Article(url, language='zh')  # Chinese

a.download()
ticks1 = time.time()
a.parse()

print(ticks1 - ticks)
print('title')
print(a.title)

print('text')
print(a.text)
print(a.authors)
print(a.publish_date)
ticks2 = time.time()
print(ticks2 - ticks1)
sina_paper = newspaper.build('http://www.sina.com.cn/', language='zh')
# url = sina_paper.articles[0].url.replace(' ', '')
# article = Article(url, language='zh')
# article.download()
# article.parse()
# print(article.text)
# for category in sina_paper.category_urls():
#     print(category)
count = 0
for ab in sina_paper.articles:

    url = ab.url.replace(' ', '')
    abc = Article(url, language='zh')
    abc.download()
    abc.parse()
    print(abc.text)
    count += 1
    print(count)
