#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: apis.py
@time: 2016/8/2 23:23
"""

"""
JSON API definition.
"""

import json,logging,inspect,functools

class APIError(Exception):
    def __init__(self,error,data="",message=""):
        super(APIError, self).__init__(message)
        self.error = error
        self.data=data
        self.message=message

class APIValueError(APIError):
    def __init__(self,field,message=""):
        super(APIValueError,self).__init__("value:invalid",field,message)

class APIResourceNotFoundError(APIError):
    def __init__(self,field,message=""):
        super(APIResourceNotFoundError,self).__init__("value: not found", field,message)

class APIPermissionError(APIError):
    def __init__(self,message=""):
        super(APIPermissionError,self).__init__('permission:forbidden','permission',message)

def main():
    print("do sth")


if __name__ == '__main__':
    main()

