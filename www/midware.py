#!/usr/bin/env python
# encoding: utf-8


"""
@description: 拦截器

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: midware.py
@time: 2016/10/3 18:00
"""

import logging

logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web
import time
from datetime import datetime
import json


def datetime_filter(t):
    delta = int(time.time() - t)
    s = ''
    if delta < 60:
        s = u'一分钟前'
    elif delta < 3600:
        s = u'%s分钟前' % (delta // 60)
    elif delta < 86400:
        s = u'%s小时前' % (delta // 3660)
    elif delta < 604800:
        s = u'%s天前' % (delta // 86400)
    else:
        dt = datetime.fromtimestamp(t)
        s = u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request: %s %s ' % (request.method, request.path))
        return (yield from handler(request))

    return logger


@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        r = yield from handler(request)

        if isinstance(r, web.StreamResponse):
            return r
        elif isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        elif isinstance(r, str):
            resp = web.Response(body=r.encode())
            resp.content_type = 'text/html;chatset=utf-8'
            return resp
        elif isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode())
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode())
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        else:
            resp = web.Response(body=str(r).encode())
            resp.content_type = 'text/plain;charset=utf-8'
            return resp

    return response


def main():
    print("do sth")


if __name__ == '__main__':
    main()
