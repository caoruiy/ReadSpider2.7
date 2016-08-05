# -*- coding:utf-8 -*-
from time import sleep

from bs4 import BeautifulSoup

from request.dload import dload,basedoc
from save.excel import Excel
from os.path import realpath
import json
import traceback


class Index(object):

    def __init__(self, **kw):
        self.excel = None
        self._dl = None
        self._config(**kw)

    def _config(self, **kw):
        """"
        配置参数
        """
        if len(kw) == 0:
            self._exit("配置参数不能为空")
        try:
            # 需要保存的文件名称（可以包含路径）
            self.file = kw['file'] or None
            # excel表格需要保存的标题信息
            self.title = kw['title'] or []

            if 'rebuild' not in kw.keys():
                kw['rebuild'] = None
            if 'from'not in kw.keys():
                kw['from'] = None
            if 'end' not in kw.keys():
                kw['end'] = None
            if 'amount' not in kw.keys():
                kw['amount'] = None
            if 'maxfor' not in kw.keys():
                kw['maxfor'] = None
            if 'request' not in kw.keys():
                kw['request'] = None
            if 'runlist' not in kw.keys():
                kw['runlist'] = None
            # 当file指定的Excel存在时，是否重建
            # 即，对已存在的Excel写入方式是重写还是追加
            self.rebuild = kw['rebuild'] or False
            # 开始抓取页码
            self.from_ = kw['from'] or 1
            # 抓取结束页码
            self.end_ = kw['end'] or None
            # 每个文件中保存多少页数据
            self.amount = kw['amount'] or 1
            # 最多保存多少个文件
            self.maxfor = kw['maxfor'] or 1
            # request请求参数
            self.request = kw['request'] or {}
            # 请求的网址
            self.url = kw["url"] or None
            self.runlist = kw['runlist'] or None

        except Exception as e:
            self._exit(e)

        # 格式判断

        # title格式
        if not isinstance(self.title, list):
            self._exit("[格式错误：] Excel表格的标题(title)必须是一个list列表")
        # 初始化
        self._init()

    def _init(self):
        """
        初始化
        """
        # 基本的数据检查
        if self.from_ <= 0  or self.amount <= 0 or self.maxfor <= 0:
            self._exit("以下参数必须是大于0的整数：\nfrom : %s\nend : %s\namount : %s\nmaxfor : %s" % (self.from_, self.end_ , self.amount, self.maxfor))
        if self.end_ and self.from_ >= self.end_:
            self._exit("抓取页码需要一个范围，而不是：(%s, %s)" % (self.from_, self.end_))
        for i in self.runlist:
            if i[0] >= i[1]:
                self._exit("抓取页码需要一个范围，而不是:" % self.runlist)
        if len(self.file.split(".")) > 2:
            self._exit("文件名中不能包含\" . \"")
        # 设置默认请求头
        self._set_header()
        if not self.data():
            self._exit("data方法必须重写")
        # 实例化Excel
        # self.excel = self._create_excel()

        # 实例化cookies
        if self.request['cookies'] and isinstance(self.request['cookies'], str):
            dl = self._get_dl()
            self.request['cookies'] = dl.get_cookie_from_file(realpath(self.request['cookies']))

    def _get_dl(self):
        if not self._dl:
            self._dl = dload(islog=True, console=True)
        return self._dl

    def _run(self):
        """
        启动抓取程序
        """
        num = self.from_ % self.amount
        from_page = self.from_ - num
        end_page = from_page + self.amount
        maxfor = self.maxfor
        # 如果数据量不够一篇文档，就不循环了
        if self.end_ and self.end_ < end_page:
            end_page = self.end_
            maxfor = 2
        for i in range(1, maxfor):
            file_name = self._create_excel()
            print('--------------------新表------------------------------')
            print(file_name)
            sleep(2)
            for page in range(self.from_, end_page):
                if self.end_ and page > self.end_:
                    print("-------------数据抓取结束-----------------------")
                    # 清理一些数据
                    excel = None
                    return False
                print(u"当前第 " + str(page) + u" 页")
                dl = self._get_dl()
                self.doc = dl.request(url=self.url, data=self.data(), callback=None, **self.request)
                self.callback()
                sleep(0.5)
            excel = None
            from_page += self.amount
            end_page += self.amount
            page = from_page

    def run(self):
        if self.runlist and isinstance(self.runlist,list):
            for i in self.runlist:
                self.from_, self.end_ = i
                self._run()
        else:
            self._run()

    def data(self):
        return None

    def callback(self):
        """返回请求内容"""
        soup = BeautifulSoup(self.doc, 'lxml')
        return soup


    def _create_excel(self):
        """
        创建Excel
        :return:
        """
        num = self.from_ % self.amount
        from_ = self.from_ - num
        end_ = from_ + self.amount
        file_ = self.file
        if file_.endswith(".xlsx") or file.endswith(".xls"):
            file_list = file_.split(".", 2)
            file_ = file_list[0]+"_%s_%s."+file_list[1]
        else:
            file_ += "_%s_%s.xlsx"
        file_ = file_ % (from_, end_)
        self.excel = Excel(file_ , rebuild=self.rebuild)
        self.excel.title(self.title)
        return  self.excel.file

    def _set_header(self):
        """包含默认请求头信息"""
        default_hearder = {
            'Accept':'*/*',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
        }
        if self.request['headers']:
            self.request['headers'] = dict(default_hearder, **self.request['headers'])
        else:
            self.request['headers'] = default_hearder

    def write(self,row, col=None, content=None, sheet=None):
        """
        写入Excel
        """

        self.excel.write(row, col, content, sheet)

    def save(self):
        """
        保存Excel
        """
        print(u"在" + str(self.excel._last_row) + u"行开始写入...")
        self.excel.save()

    def _exit(self, msg):
        """
        打印错误并退出
        :param msg: 错误信息
        """
        print("[index error:]")
        print(msg)
        print traceback.format_exc()
        exit()

