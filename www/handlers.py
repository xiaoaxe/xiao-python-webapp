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

import hashlib
import re
import time

from aiohttp import web

from apis import *
from config import configs
from coroweb import get, post
from models import Blog, User, next_id

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


@post('/api/blogs')
def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot by empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot by empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot by empty.')
    user = request.__user__
    blog = Blog(user_id=user.id, user_name=user.name, user_image=user.image, name=name.strip(), summary=summary.strip(),
                content=content.strip())
    yield from blog.save()
    return blog


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
