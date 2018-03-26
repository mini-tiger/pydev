# -*- coding: utf-8 -*-
'''
提取66影视，电视剧 下载链接，从
'''

import requests
import re


class Util(object):

    def __init__(self, *args, **kwargs):
        self.url = kwargs['url']
        self.Drama = kwargs['Drama']
        self.main()

    def get_htmlcode(self, method='get', json=None, data=None):
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
        }

        # url = self.url if self.url.rfind(
        # '/', -2) > 0 else self.url + '/'  # 如果结尾 不是/
        url = self.url
        res = requests.request(
            method, url, headers=headers, json=json, data=data)
        res.encoding = 'gb2312'   #返回 编码 设置
        print res.apparent_encoding ## 查看返回 编码
        if res.status_code == 500:
            print res
            print dir(res)
        else:
            # res = requests.get(url,headers=headers, auth=('admin','admin' ))
            print requests.utils.get_encodings_from_content(res.text) ## 查看返回 编码
            return res.text

    def get_link(self):
        return re.compile(
            '\<a.*href="(ed2k:.*)"\>(.*)\</a\>').findall(self.data)


    def main(self):
        self.data = self.get_htmlcode()
        r = re.compile('([0-9]{1,2})\..*')

        _Drama_l = filter(lambda i: int(r.findall(i[1])[0]) > self.Drama, self.get_link())
        # for i in self.get_link():
        # print u'链接地址: {}, 文件名: {}'.format(i[0],i[1])
        # 匹配集数
        sd = set()
        # for d in _Drama_l:
        #     sd.add(setd[0])
        map(lambda x:sd.add(x[0]), _Drama_l)
        for uri in sd:
            print uri

if __name__ == '__main__':

    ss = Util(url='http://www.dygang.net/dsj/20171207/JSLM2.htm',Drama=33)
