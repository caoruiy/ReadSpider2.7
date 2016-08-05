# -*- coding:utf-8 -*-
'''
Created on 2016年7月9日

实现类似于PHP中的常用方法
@author: caorui
'''

def empty(v=''):
    '判断一个对象是否为空'
    if v == None or ( len(v) == 0 and not bool(v) ):
        return True
    return False

def isset(obj,attr):
    '判断一个对象是否设置了某属性'
    try:
        if hasattr(obj, '__iter__'):
            return attr in obj
        else:
            return hasattr(obj, attr)
    except Exception:
        return False
    else:
        return True
