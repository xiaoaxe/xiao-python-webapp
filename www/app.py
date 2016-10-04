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

import os

from jinja2 import Environment, FileSystemLoader

from orm import create_pool
from midware import *
from coroweb import add_routes, add_static


def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
            autoescape=kw.get("autoescape", True),
            block_start_string=kw.get('block_start_string', '{%'),
            block_end_string=kw.get("block_end_string", "%}"),
            variable_start_string=kw.get("variable_start_string", '{{'),
            variable_end_string=kw.get("variable_end_string", '}}'),
            auto_reload=kw.get("auto_reload", True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        # path = FileSystemLoader('templates')
    logging.info("set jinja2 template path: %s" % path)

    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get("filters", None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f

    app["__templating__"] = env


def init(loop):
    yield from create_pool(loop, **configs.db)

    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, response_factory
    ])

    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)

    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()


if __name__ == '__main__':
    main()
