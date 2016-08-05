# -*- coding:utf-8 -*-
# 入口文件
import json
from os.path import realpath
from time import sleep

from request.dload import dload,basedoc
from save.excel import Excel

excel = None
def create_excel(from_page, end_page):
    global excel
    file_name = "C://Excel/luoji_" + str(from_page) + "_" + str(end_page) + ".xlsx"
    # 以追加的方式打开文件
    excel = Excel(file_name, rebuild=False)
    excel.title([u"姓名", u"手机号码", u"地址", u"车型", u"车牌号码", u"车长", u"吨位", u"始发地", u"目的地", u"罗计ID"])
    return excel.file

@basedoc
def cal(doc):
    global excel
    try:
        doc = doc.p.get_text()
    except:
        print("网络中断，已停止")
        exit()
    try:

        data = json.loads(doc, encoding="utf-8")
    except:
        print("--------------无法解析JSON---------")
        return False
    # print data
    if not data['code']:
        data = data['values']['pageResult']['content']
        if len(data) == 0:
            print("没有更多数据啦....")
            exit()
        for item in data:
            if not isinstance(item, dict) or (item['vehicle'] == None):
                continue
            loc_list = [
                item["driverName"],
                item['phone'],
                item['vehicle']['address'],
                item['typeName'],
                item['vehicleNum'],
                item['vehicle']['lengthWithUnit'],
                item['vehicle']['capacityWithUnit'],
                item['beginAddress'],
                item['endAddress'],
                item['id']
            ]
            excel.write(loc_list)
        excel.save()

    else:
        print(u"获取数据失败，请检查代码 : 网站提示：")
        print(data['values']['message'])
        print("-------------------------休眠十秒---------------------------")
        sleep(10)

    
dl = dload(islog=True,console=True)
cookies = dl.get_cookie_from_file(realpath("C://Cookies/luoji_cookie.json"))
header = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Referer':'http://www.loji.com/logistics/search?username=17788353285&requestUri=%2Flogin',
    # 'Host':'hb.crm2.qq.com',
}

def run(page, count, last_page=None,  maxfor=20):
    if last_page and last_page <= page:
        print("页码需要一个范围，谢谢")
        exit()
    global excel
    num = page % count
    from_page = page - num
    end_page = from_page + count
    # 如果数据量不够一篇文档，就不循环了
    if last_page and last_page < end_page:
        end_page = last_page
        maxfor = 2
    for i in range(1, maxfor):
        if not excel:
            file_name = create_excel(from_page, end_page)
            print('--------------------新表------------------------------')
            print(file_name)
        else:
            print("--------------无法创建新表------------------------------")
            exit()
        sleep(2)
        for page in range(page, end_page):
            if last_page and page > last_page:
                print("-------------数据抓取结束-----------------------")
                # 清理一些数据
                excel = None
                return  False
            print(u"当前第 " + str(page) + u" 页")
            dl.request('http://www.loji.com/vehicleteam/search', "page=" + str(page), cal, cookies=cookies,
                       headers=header)  # headers
            sleep(0.5)
        excel = None
        from_page += count
        end_page += count
        page = from_page


#
if __name__ == '__main__':
    # 开始编号
    # 每篇文档收录多少页数据
    run(14800,200)

# 备忘
# 漏掉的数据：
# 1800 - 2000 √
# 2200 - 2600 √
# 2800 - 3400 √
# 3600 - 4400 √
# 4600 - 5600 √
# 5800 - 7000 √
# 7200 - 8600
# 8800 - 9000 数据不齐
