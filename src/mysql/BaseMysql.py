# -*- coding=utf-8 -*-

try:
    import MySQLdb
except Exception as e:
    print('\033[1;31;0m'+"[Import Error]:"+'\033[0m'+" The imported modules are not exist: "+str(e))


# MyDQLdb操作类的基本封装，对MySQL操作流程进行统一封装
# 实现基本的增删改查
class BaseMysql(object):
    # 数据库连接对象
    _conn = None

    # 当前操作的数据表名称
    _table = None

    # select-SQL
    _select_sql = "SELECT {cols} FROM {table} WHERE {where} "

    # insert-SQL
    _insert_sql = "INSERT INTO {table}({cols}) values({values}) "

    #update-SQL
    _update_sql = "UPDATE {table} {sets} WHERE {where} "

    #insert_update-SQL
    _insert_update_sql = "INSERT INTO {table}({cols}) values({values}) ON DUPLICATE KEY UPDATE {updates} "

    #delete-SQL
    _delete_sql = "DELETE FROM {table} WHERE {where}"

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            self._conn_args = args
            self._conn_kwargs = kwargs

    def _connect(self,  *args, **kwargs):
        """
        连接数据库
        常用的连接参数：host port user passwd db charset
        """
        if not self._conn:
            self._conn = MySQLdb.connect(*args, **kwargs)
        self._cursor = self._conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        return self._conn

    def _del_table(self, table):
        """
        处理数据库表名
        """
        if self._table:
            return self._table
        if table and isinstance(table, str):
            self._table = table
        else:
            raise SQLException("table name must be a string,but local table name is :"+str(table))

    def _del_col(self, cols):
        """
        把列字典转换成字符串
        :param cols: 可选参数，查询的列字典，默认为"*"
        该参数接受一个list
        eg：['id', 'name', 'gread g']    表示查询id, name, gread三列数据，其中gread设置别名为“g”,写法可以为“列名 别名”或“列名 AS 别名”

        :return: 列字符串
        """
        if cols == None:
            return "*"
        else:
            return ",".join(cols)

    def _where_add_marks(self, value):
        """
        为SQL where部分的值添加引号
        eg：“!=张三”转化成 “!='张三'”
        """
        mark = value[1:2]
        if mark == '=':
            mark = 2
        else:
            mark = 1
        if value[0:4] == 'like':
            mark = 4
        return value[0:mark] + " '" + value[mark:].strip() + "'"

    def _del_where(self, where):
        """
        处理where条件
        :param where: 可选参数，查询条件。默认为"true",不限制查询条件，该参数接受一个字典
        eg：{and : { id : ">5" , 'or' : { 'name' : '!="张三"'} }}  该条件等于 ： (id>5 or name!='张三')
        :return: where字符串
        """
        if where == None:
            return 'true'
        else:
            wstr = ''
            for key in where:
                if isinstance(where[key], dict):
                    if wstr == '':
                        wstr += " " + self._del_where(where[key])
                    else:
                        wstr += " " + key + " " + self._del_where(where[key])
                else:
                    wstr += " " + key + " " + self._where_add_marks(where[key])

            return "(" + wstr + " )"

    def _del_group(self, group):
        """
        处理分组 条件
        :param group: 可选参数，查询分组，默认不分组,该参数接受一个list或tuple
        eg：（'id','name'）    表示以id和name分组
        :return: 分组字符串
        """
        if group == None:
            return False
        else:
            return ",".join([key +" "+ group[key] for key in group])

    def _del_having(self, having):
        """
        处理orderby子句的having选项
        """
        return self._del_where(having)

    def _del_order(self, order):
        """
        处理order选项
        """
        if isinstance(order,dict):
            return self._del_group(order)
        else:
            return ",".join([str(key+1)+" "+item for key, item in enumerate(order)])

    def _del_limit(self, limit):
        """
        处理limit选项
        :param limit: 可选参数，限制数据量或分页，默认不惜限制，输出所以查询数据，该参数接受一个大于0的整数，或者一个二值list或tuple
        eg：10   表示只显式查询结果的前10条数据
        eg：(2, 10)  表示输出第二页的10条数据
        """
        if isinstance(limit, int):
            return str(limit)
        page = limit[0]
        line = limit[1]
        if isinstance(page, int) and isinstance(line, int):
            return str(page)+","+str(line)
        else:
            raise SQLException("Limit must be an integer or two value integer tuple or list which value must greater than zero")

    def select(self, table=None, cols=None, where=None, group=None, order=None, having=None, limit=None, console=False):
        """
        查询数据库
        :param table: 表名

        :param cols: 可选参数，查询的列字典，默认为"*"
        该参数接受一个list
        eg：['id', 'name', 'gread g']    表示查询id, name, gread三列数据，其中gread设置别名为“g”,写法可以为“列名 别名”或“列名 AS 别名”

        :param where: 可选参数，查询条件。默认为"true",不限制查询条件，该参数接受一个字典
        eg：{and : { id : ">5" , 'or' : { 'name' : '!="张三"'} }}  该条件等于 ： (id>5 or name!='张三')

        :param group: 可选参数，查询分组，默认不分组,该参数接受一个字典
        eg：（'id':"DESC",'name':"ASC"）    表示以id和name分组

        :param order: 可选参数，排序
        该参数接受一个字典或者列表
        eg：['desc','asc']   表示以第一列降序，第二列升序排列
        eg：{id : 'desc', name : 'asc'}  表示以id降序 name 升序排列

        :param having: 可选参数，

        :param limit: 可选参数，限制数据量或分页，默认不惜限制，输出所以查询数据，该参数接受一个大于0的整数，或者一个二值list或tuple
        eg：10   表示只显式查询结果的前10条数据
        eg：(2, 10)  表示输出第二页的10条数据

        :param console:是否输出SQL字符串，True时输出不执行SQL，False时执行SQL
        :return:字典数据
        """
        self._del_table(table)
        cols = self._del_col(cols)
        where = self._del_where(where)
        sql = self._select_sql.format(
            cols=cols,
            table = table or self._table,
            where= where
        )
        if group:
            sql += " GROUP BY "+self._del_group(group)
        if having:
            sql +=" HAVING "+self._del_having(having)
        if order:
            sql += " ORDER BY " + self._del_order(order)
        if limit:
            sql += " LIMIT "+self._del_limit(limit)
        if console:
            return sql
        else:
            return self.exec_sql(sql)

    def insert(self, table=None, cols=None, console=False):
        """
        插入数据
        :param table: 插入数据表名
        :param cols: 插入字段
        :param console: 是否打印SQL语句
        :return: sql语句或者插入结果
        """
        self._del_table(table)
        if not cols:
            raise SQLException("cols and values must be point out in insert SQL, so cols argument can't be empty")
        sql = self._insert_sql.format(
            cols=",".join([str(item) for item in cols]),
            table=table or self._table,
            values=",".join(["'"+str(cols[item])+"'" for item in cols])
        )
        if console:
            return sql
        else:
            return self.exec_sql(sql)

    def update(self, table=None, sets=None, where=None, order=None, limit=None, console=False):
        """
        更新数据
        :param table: 表名
        :param sets: 更新字段字典
        :param where: 更新条件
        :param order: 排序
        :param limit: 限制更新条数
        :param console: 是否输出SQL语句
        :return:
        """
        self._del_table(table)
        if not sets:
            raise SQLException("'SET' must be point out in update SQL, so sets argument can't be empty")
        sql = self._update_sql.format(
            table=table or self._table,
            sets=",".join([" SET "+item+"='"+str(sets[item])+"'" for item in sets]),
            where=self._del_where(where)
        )
        if order:
            sql += " ORDER BY " + self._del_order(order)
        if limit and isinstance(limit, int):
            sql += " LIMIT " + str(limit)
        if console:
            return sql
        else:
            return self.exec_sql(sql)

    def delete(self, table=None, where=None, order=None, limit=None, console=False):
        """
        删除数据
        :param table: 表名
        :param where: 条件
        :param order: 排序
        :param limit: 限制
        :param console: 是否打印SQL
        :return:
        """
        self._del_table(table)
        if not where:
            raise SQLException("you must point out where argument in delete SQL which at least should be 'True' or 1")
        sql = self._delete_sql.format(
            table=table or self._table,
            where=self._del_where(where)
        )
        if order:
            sql += " ORDER BY " + self._del_order(order)
        if limit and isinstance(limit, int):
            sql += " LIMIT " + str(limit)
        if console:
            return sql
        else:
            return self.exec_sql(sql)

    def insert_and_update(self):
        '''
        存在数据时，更新数据
        不存在数据时，插入数据
        '''
        pass

    def exec_sql(self, sql):
        """
        执行具体的SQL语句
        :param sql:
        :return:
        """
        try:
            self._connect(*self._conn_args, **self._conn_kwargs)
            self._cursor.execute(sql)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print e
        else:
            self.rowcount = self._cursor.rowcount
            self.description = self._cursor.description
            return self._cursor.fetchall()

    def close(self):
        """
        关闭数据库连接
        """
        self._conn.close()

    def __del__(self):
        self._conn.close()

    def trans(self):
        '事务操作'
        pass


class SQLException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

# if __name__ == "__main__":
#     print("This model cann't run in main namespace")