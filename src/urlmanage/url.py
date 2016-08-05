# -*- coding:utf-8 -*-
'''
Created on 2016年7月9日

@author: caorui
'''
from collections import deque

class urlmanage(object):
    # 未访问的 URL 
    urllist = deque()
    
    # 已经访问的 URL 列表
    visited_url_list=set()
    
    def get_url(self):
        '获取一个未访问的URL'
        if len(self.urllist) > 0:
            return self.urllist.pop()
        return None

    def add_url(self,url):
        '添加未访问的 URL '
        if url not in self.urllist:
            if isinstance(url, str):
                self.urllist.append(url)
            else:
                self.urllist = self.urllist.union(url)
        return url

    def del_url(self,url):
        '删除未访问的 URL '
        self.urllist.remove(url)
        return url
    
    def clear_url(self):
        '清空待访问的 URL'
        self.urllist.clear()
    
    def list_url(self):
        '返回所有未访问的 URL列表'
        return list(self.urllist)
    
    def is_url(self,url):
        '判断 URL 是否在未访问列表当中'
        return url in self.urllist
    
    def del_and_add_to_visited(self,url=''):
        '删除访问过的url到已访问列表'
        vi_url = self.del_url(url) or url
        self.visited_url_list.add(vi_url)
        return vi_url
    
    def add_visited_url(self,url):
        '把一个 URL 添加到以访问列表'
        if isinstance(url, str):
            self.visited_url_list.add(url)
        else:
            self.visited_url_list = self.visited_url_list.union(url)
        return url
    
    def lis_visited_url(self):
        '返回所有访问过的 URL列表'
        return list(self.visited_url_list)
    
    def get_visited_url(self):
        'list_visited_url的快捷方式'
        return self.lis_visited_url()
    
    def is_visited(self,url):
        '判断 URL 是否被访问过'
        return url in self.visited_url_list
    
    def clear_visited_url(self):
        '清空已访问的 URL 列表'
        self.visited_url_list.clear()
    
            
            