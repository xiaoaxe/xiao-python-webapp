#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: app.py
@time: 2016/8/1 21:20
"""

import logging

logging.basicConfig(level=logging.INFO)

from aiohttp import web

import asyncio, os

from www.coroweb import *

from www.handlers import index

from jinja2 import Environment, FileSystemLoader

from www.midware import *


def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
            autoescape=kw.get("autoescape", True),
            block_start_string=kw.get('block_start_string', '{%'),
            block_end_string=kw.get("block_end_string", "%}"),
            variable_start_string=kw.get("variable_start_string", '{{'),
            variable_end_string=kw.get("variable_end_string", '}}'),
            auto_reload=kw.get("auto_relaod", True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
    logging.info("set jinja2 template path: %s" % path)

    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get("filters", None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app["__templating__"] = env

def init(loop):
    app = web.Application(loop=loop,middlewares=[
        logger_factory,response_factory
    ])
    init_jinja2(app,filters=dict(datetime=datetime_filter))
    add_routes(app,'handlers')
    add_static(app)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()


if __name__ == '__main__':
    main()
