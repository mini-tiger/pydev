# coding:utf-8
from __future__ import print_function
import threading
import time
maxs = 10  # 最大并发10个线程
#线程不安全，打印结果 乱序
# # 初始化信号量，数量为10，最多有10个线程获得信号量，信号量不能通过释放而大于10
threadLimiter = threading.BoundedSemaphore(maxs)


class test(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        threadLimiter.acquire()  # 获得信号量，信号量 减 1,能用的信号量变为9
        try:
            print("code one", self.name)
            time.sleep(1)  # 3秒后打印 后面的线程情况
        except:
            pass
        finally:
            threadLimiter.release()  # 释放信号量，可用的信号量 加 1

for i in range(100):
    cur = test()
    cur.start()
for i in range(100):
    cur.join()
