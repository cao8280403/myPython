#!/usr/bin/env Python
# -*- coding: utf-8 -*-
# 导入socket库:
import socket
# 创建一个socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
# s.connect(('www.kf400.cn', 80))

# # 发送数据:
# s.send('GET / HTTP/1.1\r\nHost: www.kf400.cn\r\nConnection: close\r\n\r\n'.encode(encoding="utf8"))
#
# # 接收数据:
# buffer = []
# while True:
#     # 每次最多接收1k字节:
#     d = s.recv(1024*1024).decode(encoding="utf8")
#     if d:
#         buffer.append(d)
#     else:
#         break
# data = ''.join(buffer)
#
# # 关闭连接:
# s.close()
#
# header, html = data.split('\r\n\r\n', 1)
# print(header)
# print(html)
# # 把接收的数据写入文件:
# with open('sina.html', 'wb') as f:
#     f.write(html.encode(encoding="utf8"))

s.connect(('127.0.0.1', 9999))
# 字符串前面加上b，表示bite
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah',b'exit']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()