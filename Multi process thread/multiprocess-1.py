#-*- coding: UTF-8 -*-
import multiprocessing
import time

def func(i):

        s=0
        while i > 0:
                s=s+i
                i=i-1
        print s
if __name__ == "__main__":

        pool = multiprocessing.Pool(processes = 3)  ##最多3个进程，可以根据CPU核心设置，任务绑定CPU核心
        l=[10,150,200,2]   ##4个循环，（第一个结束的任务释放核心，在处理第4个任务）一个任务只能运行一个核心上
        print time.time()

        for i in l:
                pool.apply_async(func, (i, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        pool.close()
        pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
        print time.time()