#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: hello.py
@time: 2016/8/9 13:39
"""

# !/usr/bin/env python
#  -*- coding:utf-8 -*-
# File http_post.py

import urllib
import urllib3
import json


def http_post():
    url = ''
    values = ''

    # jdata = json.dumps(values)  # 对数据进行JSON格式化编码
    http = urllib3.PoolManager()  # 生成页面请求的完整数据
    response = http.urlopen("POST", url, body=values.encode("utf-8"))  # 发送页面请求
    return response.data  # 获取服务器返回的页面信息


def main():
    resp = http_post()
    print(resp.decode("utf-8"))

def test():
    print('hello')


if __name__ == '__main__':
    # main()
    test()
