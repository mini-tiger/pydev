# coding:utf-8
import gevent
from gevent.queue import Queue
from gevent.threadpool import ThreadPool #同时并发
import os

print '当前PID {}'.format(os.getpid())



def worker(n):
    while not tasks.empty():
        task = tasks.get_nowait()
        print('Worker %s got task %s' % (n, task))
        gevent.sleep(2)

    print('Quitting time!')


def boss():
    for i in xrange(1, 25):
        tasks.put_nowait(i)

tasks = Queue()

boss()

pool = ThreadPool(10)  ##同时并发 pool是可以指定池子里面最多可以拥有多少greenlet在跑
for i in xrange(25):
    # pool.spawn(wheel)
    pool.spawn(worker, str(i))

pool.join()



# gevent.joinall([
#     gevent.spawn(worker, 'steve'),
#     gevent.spawn(worker, 'john'),
#     gevent.spawn(worker, 'nancy'),
# ])
