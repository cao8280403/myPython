#!/usr/bin/env python
# coding=utf-8
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkgeoip.request.v20200101.DescribeIpv4LocationRequest import DescribeIpv4LocationRequest

se = requests.session()


class Aliip:
    def __init__(self):
        self.url = "http://api.zhuzhaiip.com:498/GetIpPort?passageId=1335483186719006722&num=1000&protocol=2&province=&city=&minute=1&format=2&split=&splitChar=&reset=true&secret=1RN6xR"

    def requesturl(self, ip):
        client = AcsClient('LTAI4FgkhFzhjUcV6CsRU5Am', 'U7I27Sw2cQZySaMIKlyVIdKrAykprx', 'cn-hangzhou')

        request = DescribeIpv4LocationRequest()
        request.set_accept_format('json')

        request.set_Ip(ip)
        request.set_Lang("en")

        response = client.do_action_with_exception(request)
        # python2:  print(response)
        # print(str(response, encoding='utf-8'))
        return str(response, encoding='utf-8')


if __name__ == '__main__':
    test = Aliip()
    test.requesturl("49.79.11.90")
