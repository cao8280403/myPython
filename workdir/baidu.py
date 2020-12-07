from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
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
