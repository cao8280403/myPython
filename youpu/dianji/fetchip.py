#!/usr/bin/env python
#coding=utf-8
import requests
import time
import json

se = requests.session()

class Fetchip:
    def __init__(self):
        # self.url = "http://api.zhuzhaiip.com:498/GetIpPort?passageId=1335483186719006722&num=10&protocol=2&province=&city=&minute=1&format=2&split=&splitChar=&reset=true&secret=1RN6xR"
        self.url = "http://api.zhuzhaiip.com:498/GetIpPort?passageId=1335483186735783938&num=10&protocol=2&province=&city=&minute=1&format=2&split=&splitChar=&reset=true&secret=CZj0Zd"

    def requesturl(self):
        # Post_data = {
        #     'wenzhang': '床前明月光，疑是地上霜。'
        # }
        Text = se.get(self.url).text.replace("'", '"').replace('/ ', '/')
        json_obj = json.loads(Text)
        data = json_obj.get('data')
        return data



if __name__ == '__main__':
    test = Fetchip()
    test.requesturl()