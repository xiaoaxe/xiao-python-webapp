#!/usr/bin/env python
# encoding: utf-8


"""
@description: //TODO 

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: model_test.py
@time: 2016/10/3 16:06
"""

from www import orm
from www.models import *
import asyncio

@asyncio.coroutine
def test_upt(loop):
    print('start')

    # yield from orm.create_pool(user='root',password='Full77',db='nlp_web')
    #
    # u = User(name='xiao',email='123@test.com',passwd='654123',image='about:blank')
    #
    # yield from u.save()

    yield from orm.create_pool(loop, user='root', password='Full77', db='nlp_web')
    u = User(name='xiao', email='123@test.com', passwd='654123', image='about:blank')
    print(u)
    yield from u.save()

    print('end')

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_upt(loop))
    loop.close()
    if loop.is_closed():
        return

if __name__ == '__main__':
    main()
