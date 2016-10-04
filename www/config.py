#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: config.py
@time: 2016/8/2 23:49
"""

from www import config_default, config_override


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    r = {}
    for k,v in defaults.items():
        if k in override:
            if isinstance(v,dict):
                r[k]=merge(v,override[k])
            else:
                r[k]=override[k]
        else:
            r[k]=v

    return r

def toDict(d):
    D = Dict()
    for k,v in d.items():
        D[k] = toDict(v) if isinstance(v,dict) else v
    return D

configs = config_default.configs

try:
    import config_override
    configs=merge(configs, config_override.configs)
except ImportError:
    pass

configs= toDict(configs)

def main():
    print("do sth")


if __name__ == '__main__':
    main()
