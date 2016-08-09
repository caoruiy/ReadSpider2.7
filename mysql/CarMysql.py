# -*- coding=utf-8 -*-
from .BaseMysql import BaseMysql

# Mysql实际操作类，该类继承自BaseMysql
# 是对货车信息的实际操作类

# host:
# 10.1.13.110
# 192.168.1.102


class CarMysql(BaseMysql):

    def __init__(self):
        BaseMysql.__init__(self, host="10.1.13.110", port=3306, user="away", passwd="away", db="carboat", charset="utf8")
        self._table = 'car'
        self._temp_dir = "C://RedSpider2.7/mysql/"

    def set_cols(self,cols):
        desc = self.desc()


