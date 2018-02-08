# -*- coding: utf-8 -*-
'''
Created on 2016/6/30

@author: wwhhff11
'''

from gevent import monkey
import gevent
import urllib2
from time import time
from gevent.pool import Pool
from gevent.threadpool import ThreadPool
from gevent.queue import JoinableQueue, Empty

queue = JoinableQueue()
STOP="stop"

monkey.patch_all()

def html_reader():
    while True:
        try:
            url=queue.get(0)
            print 'GET: %s' % url
            respone = urllib2.urlopen(url)
            data = respone.read()
            print '%d bytes received from %s.' % (len(data), url)
        except Empty:
            break

start=time()
pool=ThreadPool(10)
for i in range(100):
    queue.put("http://www.qq.com")
for i in xrange(10):
    pool.spawn(html_reader)
pool.join()
end=time()
print end-start