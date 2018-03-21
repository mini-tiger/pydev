# coding:utf-8
import sys

sys.path = sorted(sys.path, reverse=False)  # 把当前文件夹路径，放到最后
# print sys.path


from gevent import monkey
import gevent
import urllib2
from time import time
from gevent.pool import Pool
from gevent.threadpool import ThreadPool  #同时并发
from gevent.queue import JoinableQueue, Empty, Queue, Full

monkey.patch_all()  # 把当前程序中的所有io操作都做上标记


def html_reader(url):

    print 'GET: %s' % url
    respone = urllib2.urlopen(url)
    data = respone.read()
    print '%d bytes received from %s.' % (len(data), url)


def wheel():
    while True:
        try:
            print 'current gevent: {}'.format(gevent.getcurrent())
            # url=queue.get(0)
            url = queue.get_nowait()
            html_reader(url)
            print 'current queue size: {}'.format(queue.qsize())
        except Empty:
            # except Exception as e:

            break
        except Exception as e:
            print e


start = time()
queue = JoinableQueue(10) 
# queue = Queue(10) ##最大 size 10

while True:
    try:
        queue.put_nowait("http://www.qq.com")  # put_nowait() 相当于 put() 的无阻塞模式
        print 'current queue size: {}'.format(queue.qsize())
        # queue.put("http://www.qq.com")
    except Full:
        print 'queue full'
        break



pool = ThreadPool(10)   ##同时并发 pool是可以指定池子里面最多可以拥有多少greenlet在跑
for i in xrange(10):
    pool.spawn(wheel)


pool.join()
end = time()

print end - start
