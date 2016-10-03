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

import time

from www.coroweb import get
from www.models import Blog


# @get("/")
# @asyncio.coroutine
# def index(request):
#     users = yield from User.findAll()
#     return {
#         '__template__': 'test.html',
#         'users': users
#     }

@get('/')
def index(request):
    summary = 'i am a sample summary.'
    blogs = [
        Blog(id='3', name='something new', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='learn swift', summary=summary, created_at=time.time() - 3600),
        Blog(id='1', name='First Blog', summary=summary, created_at=time.time() - 7200)
    ]

    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }


def main():
    print("do sth")


if __name__ == '__main__':
    main()
