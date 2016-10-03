#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: handlers.py
@time: 2016/8/3 0:04
"""

import re, time, json, logging, hashlib, base64, asyncio

from www.coroweb import get, post

from www.models import User, Comment, Blog, next_id


@get("/")
def index(request):
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }


def main():
    print("do sth")


if __name__ == '__main__':
    main()
