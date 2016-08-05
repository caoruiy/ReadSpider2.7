# -*- coding:utf-8 -*-

import json
import logging
import traceback
from time import time, strftime, localtime

import requests
from bs4 import BeautifulSoup

from phputil import util


class dload(object):
        
    def __init__(self, encoding=None, islog=False, logfilename=None, console=False):
        self.encoding = encoding or 'utf-8'
        self.islog = islog
        if islog:
            loginit(logfilename, console)

    def request(self, url, data=None, callback=None, **kw):
        '''
                        接受一个请求，将根据data参数的类型决定发送post或者get请求，
                        同时callback参数接受一个回掉函数，用来处理文档，该回掉函数接受一个参数，即网页全文，
                        如果data是字符串或者是None，发送get请求，否则发送post请求
        '''
        beg_time = time()
        url = str(url)
        self.log(logging.INFO, "[BEGIN] " + url)
        if url == 'None':
            self.log(logging.ERROR,"this is a None URL\t" + url)
            return None
        try:
            if util.empty(data) or isinstance(data, str):
                doc = self.__get(url, data, **kw)
            else:
                doc = self.__post(url, data, **kw)
        except Exception:
            self.log(logging.ERROR,"connection error or overtime\t" + url)
            print( traceback.format_exc() )
            return None
            
            doc.encoding = self.encoding
        end_time = time()
        self.log(logging.INFO, "[FINISH] " + str(end_time - beg_time) + " s")
        if callback == None:
            return doc.text
        else:
            return callback(doc.text)

    def __get(self, url, data=None, **kw):
        '发送一个get请求'
        return requests.get(url, data, **kw)

    def __post(self, url, data=None, **kw):
        '发送一个post请求'
        return requests.post(url, data, **kw)

    def get_cookie_from_file(self, file):
        file = open(file)
        cookies = json.load(file)
        file.close()
        return  cookies

    def log(self, level, msg):
        ''''
                        打印log日志
        CRITICAL    50
        ERROR       40
        WARNING     30
        INFO        20
        DEBUG       10
        NOTSET      0
        '''
        if not self.islog:
            return None
        if level >= logging.CRITICAL:
            logging.critical(msg)
        elif level >= logging.ERROR:
            logging.error(msg)
        elif level >= logging.WARNING:
            logging.warning(msg)
        elif level >= logging.INFO:
            logging.info(msg)
        elif level >= logging.DEBUG:
            logging.debug(msg)
        else:
            logging.log(logging.NOTSET, msg)
    
    
def basedoc(fun):
    '简单的网页内容装饰器，返回网页的BeautifulSoup对象'
    def deal_doc(doc):
        soup = BeautifulSoup(doc, 'lxml')
        return fun(soup)
    return deal_doc

def loginit(logfilename, console):
    '初始化日志信息'
    def init(logfilename, console):
        log_dir = 'log/'
        filename = logfilename or strftime('%Y-%m-%d', localtime(time()))
        logging.basicConfig(
                            filename=log_dir + filename + '.log',
                            filemode='a',
                            format='%(asctime)s %(levelname)s %(message)s',
                            # %(filename)s[line:%(lineno)d] # 隐藏文件名和行号
                            level=logging.NOTSET,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            )
        error_log = logging.FileHandler(filename=log_dir + filename + '_error.log')
        error_log.setLevel(logging.ERROR)
        error_log.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'))
        logging.getLogger().addHandler(error_log)   
        if console:
            console_log = logging.StreamHandler()
            console_log.setLevel(logging.ERROR)
            console_log.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
            logging.getLogger().addHandler(console_log)
    init(logfilename, console)
    








    
