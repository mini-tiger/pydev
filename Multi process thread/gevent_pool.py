# coding:utf-8
import sys

sys.path=sorted(sys.path,reverse=False)  #把当前文件夹路径，放到最后
# print sys.path


from gevent import monkey
import gevent
import urllib2
from time import time
from gevent.pool import Pool
from gevent.threadpool import ThreadPool
from gevent.queue import JoinableQueue, Empty

queue = JoinableQueue()
STOP="stop"

monkey.patch_all() ## 把当前程序中的所有io操作都做上标记

def html_reader(url):

    print 'GET: %s' % url
    respone = urllib2.urlopen(url)
    data = respone.read()
    print '%d bytes received from %s.' % (len(data), url)


def wheel():
    while True:
        try:
            print gevent.getcurrent()
            url=queue.get(0)
            html_reader(url)
        except Empty :    
        # except Exception as e:
            break



start=time()
pool=ThreadPool(5)
for i in range(10):
    queue.put("http://www.qq.com")
for i in xrange(5):
    pool.spawn(wheel)
pool.join()
end=time()

print end-start