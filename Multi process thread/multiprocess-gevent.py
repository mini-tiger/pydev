#-*- coding: UTF-8 -*-
from multiprocessing import cpu_count, Queue, JoinableQueue, Pool, current_process
import time
from gevent import monkey
monkey.patch_all(thread=False)
import gevent
import datetime
from Queue import Empty

t = time.time()


def util(x):
    start_time = t
    l = [x for x in range(7777777 + x) if x % 2 == 0 and x % 3 == 0]
    print 'result : {},use time: {} pid: {}'.format(str(sum(l)), time.time() - start_time,current_process().pid)


def func(n):
    gevent.joinall([gevent.spawn(util, x) for x in range(n)])


def start_process():
    print 'Starting', current_process().name,'pid',current_process().pid

if __name__ == "__main__":

    pool = Pool(processes=cpu_count() * 2,
                initializer=start_process, maxtasksperchild=10)

    st = t
    n = 16
    pool.map(func(10), range(n))  # 启动n 个进程,每个里面10个 协程
    pool.close()
    pool.join()

    print 'totle use time:' + str(time.time() - st)
