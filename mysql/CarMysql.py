# -*- coding=utf-8 -*-
import re

from mysql.BaseMysql import BaseMysql


# Mysql实际操作类，该类继承自BaseMysql
# 是对货车信息的实际操作类

# host:
# 10.1.13.110
# 192.168.1.102


class CarMysql(BaseMysql):

    def __init__(self):
        BaseMysql.__init__(self, host="10.1.13.110", port=3306, user="away", passwd="away", db="carboat", charset="utf8")
        self._table = 'car'

    def add(self,item):
        """
        添加一条新的数据
        :param item:
        :return:
        """
        keys = ["name", "mobile", "address", "cartype", "carid", "carlength", "stowage", "oftenAddress", "beginAddress",
                "endAddress", "luojiID", "position", "lngLat", "img"]
        cols = {key : val for key, val in zip(keys,item)}
        address = re.match(u"^中国(.*?省)*(.*?市)*(.*?[区|县|乡])*", cols['address'])
        if address:
            groups = address.groups()
            if groups[0]:
                cols['province'] = groups[0]
            if groups[1]:
                cols['city'] = groups[1]
            if groups[2]:
                cols['area'] = groups[2]
        self.insert(cols=cols)
        return self.rowcount

