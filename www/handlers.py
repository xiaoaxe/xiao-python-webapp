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

from www.coroweb import get, post
from www.models import Blog, User
from www.apis import *
from www.models import next_id
import re
import hashlib
from aiohttp import web
import json
from conf.config import configs
import logging

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\_\-]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

COOKIE_NAME = configs.session.cookiename
_COOKIE_KEY = configs.session.secret


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


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


@get('/signout')
def signout(request):
    referer = request.header.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user sign out.')
    return r


@get('/api/users')
def api_get_users():
    users = yield from User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'

    return dict(users=users)


@post('/api/users')
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = yield from User.findAll('email=?', email)
    if len(users) > 0:
        raise APIError('regester failed', email, 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='http://www.gravatar.com/acatar/%s?d=mm&s=120' % hashlib.md5(email.encode()).hexdigest())
    yield from user.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode()
    return r


@post('/api/authenticate')
def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid passwd.')
    users = yield from User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'email not exist.')
    user = users[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode())
    sha1.update(b':')
    sha1.update(passwd.encode())
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid passwd')

    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode()
    return r


# 计算加密的cookie
def user2cookie(user, max_age):
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode()).hexdigest()]
    return '-'.join(L)


# @get('/api/users')
# def api_get_users(*,page='1'):
#     page_index = get_page_index(page)
#     num = yield from User.findNumber('count(id)')
#     p = Page(num,page_index)
#     if num ==0:
#         return dict(page=p,users=())
#     users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset,p.limit))
#     for u in users:
#         u.passwd = '******'
#         return dict(page=p,users=users)


def main():
    print("do sth")


if __name__ == '__main__':
    main()
