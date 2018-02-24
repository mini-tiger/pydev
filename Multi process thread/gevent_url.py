# coding:utf-8
import sys

sys.path=sorted(sys.path,reverse=False)  #把当前文件夹路径，放到最后
print sys.path

from gevent import monkey
monkey.patch_all()
import gevent
import urllib2


def f(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))

gevent.joinall([
	    gevent.spawn(f, 'https://www.yahoo.com/'),
        gevent.spawn(f, 'https://www.python.org/'),

        gevent.spawn(f, 'https://github.com/'),
])