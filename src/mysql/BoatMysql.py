# -*- coding=utf-8 -*-
from .BaseMysql import BaseMysql

# Mysql实际操作类，该类继承自BaseMysql
# 是对货船信息的实际操作类


class BoatMysql(BaseMysql):

    def __init__(self):
        BaseMysql.__init__(self, host="192.168.1.102", port=3306, user="away", passwd="away", db="carboat", charset="utf8")
        self._table = 'boat'
