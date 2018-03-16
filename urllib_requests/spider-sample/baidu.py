# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import os
from gevent import monkey
monkey.patch_all()
import gevent


try:
    # 自定义 客户端 浏览器版本
    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'
    # headers = {'User-Agent': user_agent}
    url = 'https://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs3&word=%E7%BE%8E%E5%BE%97%E8%AE%A9%E4%BA%BA%E7%AA%92%E6%81%AF%E7%9A%84%E9%A3%8E%E6%99%AF&oriquery=%E9%A3%8E%E6%99%AF&ofr=%E9%A3%8E%E6%99%AF&ctd=1521161928287^00_1349X330&sensitive=0'
    r = urllib2.Request(url)
    r.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(r, timeout=30)  # 超时时间
except urllib2.URLError as e:  # 与 except Exception as e:  效果一样
    print e
    print e.code
    print e.info()
    print e.geturl()
    print e.read()
else:
    print response.geturl()  # 当前URL
    print response.info()  # 服务端信息
    data = response.read()  # 页面信息
finally:
    print '请求页面数据完毕'


# with open('1.html','w') as f:
# 	f.write(data)
urls = re.findall(r'data-imgurl="(.*?)"', data)  # python 3  data.decode()
print urls
index = 0


url_list = []
for url in urls:
    index += 1
    if re.search('.jpg$', url):
        picname = os.path.join(os.getcwd(), 'pic' + str(index) + '.jpg')

    url_list.append((url, picname))


def func(url, picname):
    try:
        urllib.urlretrieve(url, picname)
        print '正在下载 {}'.format(picname)
    except Exception as e:
        print '错误下载 {}'.format(picname)
    finally:
        print '完成下载 {}'.format(picname)


gevent.joinall(map(lambda x: gevent.spawn(func(x[0], x[1])), url_list))


