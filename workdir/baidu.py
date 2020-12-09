from urllib.parse import quote
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
request = requests.get("http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=88d304d14273946c00cd3cabc7d25199&orderNo=GL20201208142456Pe5sEDu6&count=2&isTxt=0&proxyType=1")
text =  json.loads(request.text)
for key in text:
    print(str(key)+':'+str(text[key]))

for (key,value) in text.items():
    print(str(key)+':'+str(value))

port=0
ip=0
obj = text["obj"]
obj_length = obj.__len__
for obj_dict in obj:
    port = obj_dict['port']
    ip = obj_dict['ip']
    print(port,ip)


chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=http://"+ip+":"+port)
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(options=chromeOptions)

browser.set_window_size(1024,768)  # 分辨率 1024*768
# 查看本机ip，查看代理是否起作用
browser.get("http://httpbin.org/ip")
print(browser.page_source)

# 退出，清除浏览器缓存
browser.quit()



request = requests.get("https://www.atool99.com/useragent.php")
print(request.text)


def parseBaidu(keyword, pagenum):
    keywordsBaseURL = 'https://www.baidu.com/s?wd=' + str(quote(keyword)) + '&oq=' + str(quote(keyword)) + '&ie=utf-8' + '&pn='
    pnum = 0
    while pnum <= int(pagenum):
        baseURL = keywordsBaseURL + str(pnum*10)
        try:
            request = requests.get(baseURL, headers=headers)
            soup = BeautifulSoup(request.text, "html.parser")
            for a in soup.select('div.c-container > h3 > a'):
                url = requests.get(a['href'], headers=headers).url
                yield url
        except:
            yield None
        finally:
            pnum += 1

# def parseBaidu(keyword, pagenum)

def main():
    for url in parseBaidu("400电话",10):
        if url:
            print(url)
        else:
            continue


main()
