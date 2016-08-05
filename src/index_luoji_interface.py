# -*- coding=utf-8 -*-
from index.index import Index


class LuoJi(Index):

    def __init__(self, config):
        super(LuoJi, self).__init__(**config)

    def callback(self):
        doc = super(LuoJi, self).callback()
        self.write([doc.p.get_text(),])
        self.save()

    def data(self):
        return "page="+str(self.from_)

config = {
    "url":'http://www.loji.com/vehicleteam/search',
    "runlist":[(1,3)],
    "file": "C://Excel/new/luoji.xlsx",
    "title":[u"姓名", u"手机号码", u"地址", u"车型", u"车牌号码", u"车长", u"吨位", u"始发地", u"目的地", u"罗计ID"],
    "amount":20,
    "maxfor":20,
    "request":{
        "cookies": "C://Cookies/luoji_cookie.json",
        "headers":{},
    },
}
luoji = LuoJi(config)
luoji.run()