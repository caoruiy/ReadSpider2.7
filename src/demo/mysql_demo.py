# -*- coding=utf-8 -*-

from mysql.CarMysql import CarMysql

car = CarMysql()

print(
car.select(cols=('id', 'name as xm'), where={'id': ">1"}, group={"id": "DESC", 'name': "ASC"}, having={"id": "<10"},
           order={"id": "DESC"}, limit=1))

print (car.insert(cols={'id': "10", "name": "zhangsan"}, console=True))

print (car.update(sets={"id": 1, "name": "zhang"}, order=("DESC", "ASC"), limit=10, console=True))

print (car.delete(where={"id": "=3"}, limit=1, console=True))
print car.exec_sql("select * from test")