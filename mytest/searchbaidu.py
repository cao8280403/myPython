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


def fib(max):
    vv = ' '
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        # 包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator：
        # yield b # 遇到yield就中断，下次又继续执行
        a, b = b, a + b
        n = n + 1
        vv = vv + str(b) + ' '
    return vv


var = list(range(1, 11))
var1 = [x * x for x in range(1, 11) if x % 2 == 0]
var2 = [x * x for x in range(1, 11)]
var3 = [m + n for m in 'ABC' for n in 'XYZ']
var4 = [d for d in os.listdir('.')]  # os.listdir可以列出文件和目录
d = {'x': 'A', 'y': 'B', 'z': 'C'}
var5 = [k + '=' + v for k, v in d.items()]
L = ['Hello', 'World', 'IBM', 'Apple']
var6 = [s.lower() for s in L]
var7 = fib(6)
f.write(str(var))
f.write('\n')
f.write(str(var1))
f.write('\n')
f.write(str(var2))
f.write('\n')
f.write(str(var3))
f.write('\n')
f.write(str(var4))
f.write('\n')
f.write(str(var5))
f.write('\n')
f.write(str(var6))
f.write('\n')
f.write(str(var7))
f.close()

# 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
# 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
        print(x)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break


def yanghui():
    L = [1]
    n=0
    while n<10:
        # yield L
        print(L)
        n = n +1
        L = [1] + [L[i] + L[i + 1] for i in range(len(L) - 1)] + [1]


yanghui()

