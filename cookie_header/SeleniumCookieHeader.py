# -*- coding=utf-8 -*-
import json

# 该模块用来获取页面的cookie和header信息
# 通过selenium来打开页面，输入验证码，登陆成功后获取cookie和header信息
class SeleniumCookieHeader(object):

    # 要打开的网址
    url = None

    def __init__(self):
        pass

    def init(self, url):
        self.url = url
        self.open()

    def open(self):
        pass

    def get_cookie_header(self, driver):
        cookies = driver.get_cookies()
        dict_cookie = {}
        for cookie in cookies:
            print  cookie['name']," : ", cookie['value']
            dict_cookie[cookie['name']] = cookie['value']
        try:
            file = open( "luoji_cookie.json", "w")
        except IOError as ioe:
            print str(ioe)
        else:
            json.dump(dict_cookie, file)
            file.close()

