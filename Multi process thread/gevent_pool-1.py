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
# STOP="stop"

monkey.patch_all()

def util(n):
    l=[x for x in range(n) if x % 2==0 and x %3 == 0]
    print (sum(l),)



def wheel():
    while True:
        try:
            print gevent.getcurrent()
            n=queue.get(0)
            util(n)
        except Empty :    
        # except Exception as e:
            break



start=time()
pool=ThreadPool(10)

for i in range(10):
    queue.put(7777777)


for i in xrange(10):
    pool.spawn(wheel)


pool.join()
end=time()

print end-start