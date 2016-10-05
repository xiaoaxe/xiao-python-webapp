#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: config_default.py
@time: 2016/8/2 23:46
"""

configs= {
    'debug':True,
    'db':{
        'host':'127.0.0.1',
        'port':3306,
        'user':'root',
        'password':'Full77',
        'db':'nlp_web'
    },
    'session':{
        'secret':"xiao-42",
        'name':'xiaosession'
    }

}

def main():
    print("do sth")


if __name__ == '__main__':
    main()

